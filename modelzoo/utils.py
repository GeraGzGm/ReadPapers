from enum import Enum
from typing import Optional
from dataclasses import dataclass

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torch.optim import SGD, Adam, RMSprop, Adamax
from torch.optim.lr_scheduler import ReduceLROnPlateau, StepLR

class Metrics:
    @classmethod
    def Accuracy(cls, y_true: torch.Tensor,  outputs: torch.Tensor) -> float:
        _, predicted = torch.max(outputs.data, 1)
        correct = (predicted == y_true).sum().item()
        return correct / y_true.size(0)

@dataclass
class Parameters:
    epochs: int
    batch_size: int
    val_batch_size: int
    model: nn.Module
    optimizer: torch.optim.Optimizer
    loss_function: nn.Module
    labels: Enum
    train_type: str
    datasets: tuple[DataLoader, Optional[DataLoader], DataLoader]
    inferece_transforms: list
    scheduler: Optional[torch.optim.lr_scheduler.LRScheduler] = None

@dataclass
class Output:
    inputs: torch.Tensor
    labels: torch.Tensor
    outputs: torch.Tensor
    accuracy: float

@dataclass
class Optimizers:
    sgd = SGD
    adam = Adam
    adamax = Adamax
    rmsprop = RMSprop

    @classmethod
    def get_optimizer(cls, name: str) -> torch.optim.Optimizer:
        """Get optimizer class by name."""
        try:
            return getattr(cls, name)
        except AttributeError:
            raise ValueError(
                f"Unknown optimizer '{name}'. "
                f"Available optimizers: {list(cls.__annotations__.keys())}"
            )

@dataclass
class LossFunctions:
    cross_entropy = nn.CrossEntropyLoss

    @classmethod
    def get_criterion(cls, name: str) -> nn.Module:
        """Get loss function class by name."""
        try:
            return getattr(cls, name)
        except AttributeError:
            raise ValueError(
                f"Unknown Loss Function '{name}'. "
                f"Available Loss Function: {list(cls.__annotations__.keys())}"
            )


@dataclass
class Schedulers:
    plateau = ReduceLROnPlateau
    per_epoch = StepLR

    @classmethod
    def get_scheduler(cls, name: str) -> torch.optim.lr_scheduler.LRScheduler:
        """Get scheduler class by name."""
        try:
            return getattr(cls, name)
        except AttributeError:
            raise ValueError(
                f"Unknown scheduler '{name}'. "
                f"Available schedulers: {list(cls.__annotations__.keys())}"
            )

from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    TEXT_MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.TEXT_MESSAGE.format_map(asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: ClassVar[float] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MINUTES_IN_HOUR: ClassVar[float] = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.actions_count = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.actions_count * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'''{type(self).__name__} error.
            Subclasses should implement get_spent_calories!''')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_ENERGY_SUBTRAHEND: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        duration_in_minutes = self.duration_h * self.MINUTES_IN_HOUR
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             - self.CALORIES_ENERGY_SUBTRAHEND)
            * self.weight_kg
            * duration_in_minutes
        ) / self.M_IN_KM


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_DURATION_MULTIPLIER: ClassVar[float] = 0.029
    CALORIES_MEAN_SPEED_SQUARING: ClassVar[float] = 0.003

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / (self.duration_h * self.MINUTES_IN_HOUR)

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
                + self.CALORIES_DURATION_MULTIPLIER * self.duration_h
                + self.CALORIES_MEAN_SPEED_SQUARING
                * (self.get_mean_speed() ** self.CALORIES_MEAN_SPEED_SQUARING)
                * (self.weight_kg / self.height_cm)
            )
            * self.duration_h
        ) / self.MINUTES_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_SWIMMING: ClassVar[float] = 0.002
    CALORIES_DURATION_MULTIPLIER: ClassVar[float] = 0.105

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_SWIMMING
                * self.get_distance()
                * self.weight_kg
                * self.CALORIES_DURATION_MULTIPLIER
                * self.duration_h
            )
            / self.MINUTES_IN_HOUR
        )


def run_training(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    running = Running(10000, 1.5, 70)
    sports_walking = SportsWalking(12000, 2, 65, 170)
    swimming = Swimming(2000, 0.5, 75)

    run_training(running)
    run_training(sports_walking)
    run_training(swimming)

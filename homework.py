from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Type


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
        raise NotImplementedError(f'{type(self).__name__} error. Subclasses '
                                  'should implement get_spent_calories!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_ENERGY_SUBTRAHEND: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        duration_in_minutes = self.duration_h * self.MINUTES_IN_HOUR
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_ENERGY_SUBTRAHEND
            )
            * self.weight_kg
            / self.M_IN_KM
            * duration_in_minutes
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_DURATION_MULTIPLIER: ClassVar[float] = 0.029
    CALORIES_MEAN_SPEED_SQUARING: ClassVar[float] = 2
    KM_PER_HOUR_TO_M_PER_SEC: ClassVar[float] = 0.278
    CM_TO_M: ClassVar[float] = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        return (
            ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg)
             + ((self.get_mean_speed() * self.KM_PER_HOUR_TO_M_PER_SEC) ** 2
                / (self.height_cm / self.CM_TO_M))
             * (self.CALORIES_DURATION_MULTIPLIER * self.weight_kg))
            * (self.duration_h * self.MINUTES_IN_HOUR)
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SUBTRAHEND: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool_m
            * self.count_pool
            / self.M_IN_KM
            / self.duration_h
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SUBTRAHEND)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight_kg
            * self.duration_h
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""
    training_data: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type not in training_data:
        raise KeyError(f'Тренировки {workout_type} нет в списке известных.')
    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        + f'Длительность:{self.duration: .3f} ч.; '
                        + f'Дистанция:{self.distance: .3f} км; '
                        + f'Ср. скорость:{self.speed: .3f} км/ч; '
                        + f'Потрачено ккал:{self.calories: .3f} ккал.')
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Ставим заглушку на случай вызова функции."""

        raise NotImplementedError("Метод неопределен")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_type = type(self).__name__

        return InfoMessage(training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
       Дополнительно требуется ввод роста спортсмена в сантиметрах."""

    LEN_STEP: float = 0.65
    KMperH_TO_MperMIN: float = 0.278
    CALORIES_ARG1: float = 0.035
    CALORIES_ARG2: float = 0.029
    SM_IN_M = 100

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_ARG1
                * self.weight
                + (self.get_mean_speed()
                   * self.KMperH_TO_MperMIN) ** 2
                / (self.height
                   / self.SM_IN_M)
                * self.CALORIES_ARG2
                * self.weight)
                * self.duration
                * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание.
       Дополнительно требуется ввод
       длины бассейна и числа проплвтых дорожек."""

    LEN_STEP: float = 1.38
    CALORIES_ARG1: float = 1.1
    CALORIES_ARG2: int = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_ARG1)
                * self.CALORIES_ARG2
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type not in training_type:
        raise ValueError('Неподдерживаемый тип тренировки')
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print (info.get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

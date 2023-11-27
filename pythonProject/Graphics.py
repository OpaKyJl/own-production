# импортируем нужные библиотеки
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors as mplc
from statsmodels.tsa.arima.model import ARIMA


# читаем датасет
def data_read(path_to_data):

    data = pd.read_csv(path_to_data, header=0, delimiter=',')

    # запоминаем название столбцов
    list_data_head = data.columns.values.tolist()
    # удаляем первое название столбца "datum"
    list_data_head.__delitem__(0)
    # возврашаем датасет и список названий столбцов
    return data, list_data_head


# создаём графики
def plot_graphics(file_path, name_column):
    fig, axes = plt.subplots()
    # получаем наш датасет
    timeseries = data_read(file_path)[0]

    # фильтруем датасет по выбранному столбцу данных
    timeseries = timeseries.filter(['datum', name_column])
    # преобразуем строки столбца "datum" в тип date
    timeseries['datum'] = pd.to_datetime(timeseries['datum']).dt.date
    timeseries['datum'] = pd.to_datetime(timeseries['datum']).dt.normalize()
    # выставляем строки столбца "datum" индексами
    timeseries.set_index(keys='datum', drop=True, inplace=True)
    # сжимаем размерность массив
    timeseries = timeseries.squeeze(axis=1)

    ###############################################################################
    # код для подбора параметров p d q
    # он --используется-- один раз, чтобы найти параметры p, d и q
    # данные параметры нужны для создания модели ARIMA

    # import warnings
    # warnings.filterwarnings("ignore")

    # p = range(0, 10)
    # d = q = range(0, 3)
    # pdq = list(itertools.product(p, d, q))
    # best_pdq = (0, 0, 0)
    # best_aic = np.inf
    # for params in pdq:
    #     model_test = ARIMA(timeseries, order=params)
    # result_test = model_test.fit()
    # if result_test.aic < best_aic:
    #     best_pdq = params
    # best_aic = result_test.aic
    # print(best_pdq, best_aic) #(9, 2, 2) 686.1240475778249

    p, d, q = 9, 2, 2

    ###############################################################################
    # создаём модель ARIMA
    model = ARIMA(timeseries, order=(p, d, q))
    result = model.fit()

    ###############################################################################
    # прогнозирование
    pred = result.get_prediction(start='2014-05-31', end='2021-01-31', dynamic=False)
    pred_ci = pred.conf_int()

    # отрисовка текущих данных
    ax = timeseries['2014-01-31':].plot(label='Текущие данные', color="#CB187D", drawstyle='steps-pre')
    # отрисовка предсказанных данных
    pred.predicted_mean.plot(ax=ax, label='Предсказание', alpha=.7, color="#FD831E", drawstyle='steps-pre')
    # визуализация погрешности
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='#18CA18', alpha=.2)
    # заполнение легенды
    ax.set_xlabel('Дата')
    ax.set_ylabel('Средний объём продаж')
    ax.set_title(name_column)
    # добавление сетки
    plt.grid(which='major')
    plt.grid(which='minor')
    # установка цвета фона
    fig.set_facecolor('#FFE9BE')
    plt.legend()
    # отображение данных по наведению курсора
    mplc.cursor(hover=True)
    axes.plot()
    # возвращение нашей фигуры(плота)
    return fig
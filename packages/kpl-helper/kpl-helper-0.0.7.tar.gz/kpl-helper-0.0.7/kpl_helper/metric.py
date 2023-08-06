from kpl_helper.base import _MsgType, _send_metric, get_config
import warnings
# metric plot type
PLOT_LINE = 'line'


class MetricFigure:
    def __init__(self, title, y1_name, y1_type=PLOT_LINE, y2_name=None, y2_type=None):
        warnings.warn(
            "`MetricFigure` is deprecated; use the `TensorBoard` instead")
        if not get_config().get_inner():
            return
        """
        :param title:      图表的名称(最多两个纵轴)
        :param y1_name:    metric纵轴1名称, 如 Accuracy
        :param y1_type:    metric纵轴1类型, 如 PLOT_LINE为折线图
        :param y2_name:    metric纵轴2名称, 如 Softmax_Loss
        :param y2_type:    metric纵轴2类型, 如 PLOT_LINE为折线图
        """
        self.y1_name = y1_name
        self.y2_name = y2_name
        self.title = title
        if not isinstance(title, str) and len(title) == 0:
            raise ValueError("title must be string")
        if not isinstance(y1_name, str) and len(y1_name) == 0:
            raise ValueError("y1 must be string")
        if y1_type not in (PLOT_LINE,):
            raise KeyError("y1_type not exists")
        series = [{
            "name": y1_name,
            "type": y1_type,
        }]
        if y2_name:
            if not isinstance(y2_name, str) and len(y2_name) == 0:
                raise ValueError("y2 must be string")
            if y2_type not in (PLOT_LINE,):
                raise KeyError("y2_type not exists")
            series.append({
                "name": y2_name,
                "type": y2_type,
            })
        body = {
            "msgType": _MsgType.NewMetric,
            "title": title,
            "series": series
        }
        _send_metric(body)

    def push_metric(self, x, y1, y2=None):
        if not get_config().get_inner():
            return
        """
        :param x:   横坐标，一般为迭代次数
        :param y1:  x对应的y1的值
        :param y2:  x对应的y2的值
        :return:
        """
        items = [{
            "msgType": _MsgType.MetricData,
            "title": self.title,
            "seriesName": self.y1_name,
            "value": [x, y1]
        }]
        if y2 and self.y2_name:
            items.append({
                "msgType": _MsgType.MetricData,
                "title": self.title,
                "seriesName": self.y2_name,
                "value": [x, y2]
            })
        _send_metric(items)


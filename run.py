from XJBeauty.XJBeauty import XJBeauty
from Utils.TimeElapsedCounter import TimeElapsedCounter

with TimeElapsedCounter() as tec:
    xj_beauty = XJBeauty('hello')
    xj_beauty.run()
xj_beauty._log.info(str(tec))
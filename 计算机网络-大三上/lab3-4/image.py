import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 指定默认字体
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

categories = ["丢包率 0%", "丢包率 1%", "丢包率 3%", "丢包率 6%", "丢包率 10%"]

# GBN协议，窗口=8 数据
values_bar1 = [6317.53, 5714.93, 5352.60, 5337.22, 4774.69]  # 吞吐率 bytes/ms
values_line1 = [294, 325, 347, 348, 389]  # 时延 ms

# SR协议，窗口=8 数据
values_bar2 = [6030.37, 302.402, 114.306, 51.3634, 31.1015]  # 吞吐率 bytes/ms
values_line2 = [308, 6142, 16249, 36161, 59719]  # 时延 ms

# GBN协议，窗口=16 数据
values_bar3 = [6253.71, 6069.78, 5768.18, 5337.22, 4952.94]  # 吞吐率 bytes/ms
values_line3 = [297, 306, 322, 348, 375]  # 时延 ms

# SR协议，窗口=16 数据
values_bar4 = [6170.61, 310.179, 120.537, 52.1318, 35.6600]  # 吞吐率 bytes/ms
values_line4 = [301, 5988, 15409, 35628, 52085]  # 时延 ms

fig, ax1 = plt.subplots()

# 创建柱状图
bar_width = 0.1  # 柱子的宽度
index = np.arange(len(categories))

# 添加柱状图
ax1.bar(
    index - bar_width * 1.5,
    values_bar1,
    bar_width,
    label="GBN协议，窗口=8 - 吞吐率",
    color="orange",
)
ax1.bar(
    index - bar_width * 0.5,
    values_bar2,
    bar_width,
    label="SR协议，窗口=8 - 吞吐率",
    color="green",
)
ax1.bar(
    index + bar_width * 0.5,
    values_bar3,
    bar_width,
    label="GBN协议，窗口=16 - 吞吐率",
    color="blue",
)
ax1.bar(
    index + bar_width * 1.5,
    values_bar4,
    bar_width,
    label="SR协议，窗口=16 - 吞吐率",
    color="red",
)

# 设置x轴标签和图例
ax1.set_xlabel("丢包率")
ax1.set_xticks(index)
ax1.set_xticklabels(categories)
ax1.set_ylabel("吞吐率(bytes/ms)", color="orange")
ax1.tick_params(axis="y", labelcolor="orange")
ax1.legend(loc="upper left")

# 实例化共享x轴的第二个坐标轴
ax2 = ax1.twinx()

# 添加折线图
ax2.plot(
    categories,
    values_line1,
    color="orange",
    marker="o",
    linestyle="-",
    linewidth=2,
    label="GBN协议，窗口=8 - 平均传输时间",
)
ax2.plot(
    categories,
    values_line2,
    color="green",
    marker="s",
    linestyle="--",
    linewidth=2,
    label="SR协议，窗口=8 - 平均传输时间",
)
ax2.plot(
    categories,
    values_line3,
    color="blue",
    marker="^",
    linestyle="-.",
    linewidth=2,
    label="GBN协议，窗口=16 - 平均传输时间",
)
ax2.plot(
    categories,
    values_line4,
    color="red",
    marker="*",
    linestyle=":",
    linewidth=2,
    label="SR协议，窗口=16 - 平均传输时间",
)

ax2.set_ylabel("平均传输时间(ms)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")
ax2.legend(loc="upper right")

# 显示图表
plt.tight_layout()
plt.show()

# reachcheck — 批量主机连通性巡检工具

一个用 Python 写的小工具：读取 YAML 里的一批 IP，逐个用系统 `ping` 探测连通性，结果同时打到控制台和日志文件。适合当**巡检脚本**的起点——定时跑一遍，把"哪些机器不通"记下来。

> 开发环境：Windows 10/11 + Python 3.9+。命令行依赖系统自带 `ping`（Windows 自带，无需安装）。

## 功能

- 从 `yaml_config/ips.yaml` 读取待探测 IP 列表，不用改代码
- 支持 `--yaml` 参数指定其他配置文件
- 启动时先 ping `127.0.0.1` 做自检，自检不过直接退出（避免"以为在跑、其实环境坏了"）
- 每台主机的结果写入日志文件 `logs/logginglogs.log`，同时输出到终端
- 失败原因分类记录：超时（Timeout）/ 不通（Unreachable）/ 未知错误
- Windows 与 Linux 自动切换 `ping` 参数（`-n` / `-c`）与输出编码，跨平台可用

## 项目结构

```
reachcheck/
├── main.py                  # 入口：读配置 → 自检 → 循环探测
├── logging_config.py        # 日志配置（文件 + 控制台双输出）
├── yaml_config/
│   └── ips.yaml             # 待探测的 IP 列表
├── logs/
│   └── logginglogs.log      # 运行日志（自动生成）
└── README.md
```

## 安装

```bash
git clone https://github.com/<你的用户名>/reachcheck.git
cd reachcheck
pip install -r requirements.txt
```

## 使用

> 请在项目根目录下执行，配置与日志路径都是相对路径。

```bash
# 用默认配置 yaml_config/ips.yaml
python main.py

# 指定其他配置文件
python main.py --yaml yaml_config/ips_prod.yaml
```

配置文件格式：

```yaml
ips:
  - 127.0.0.1
  - 192.168.1.10
  - 10.0.0.5
```

## 输出示例

```
2026-11-18 12:57:05 main INFO 目标IP:'127.0.0.1'状态: 自检成功
2026-11-18 12:57:05 main INFO 一共获取到4台服务器 工具自检成功 启动循环
2026-11-18 12:57:06 main INFO 目标IP: 127.0.0.1 状态: Success!
2026-11-18 12:57:09 main ERROR 目标IP: 8.8.8.8 状态: 超时 (Timeout) Error!
```

## 实现说明

- **自检**：先用 `127.0.0.1` 走一遍完整流程，确认 `subprocess` 调用和日志都正常，再批量跑。失败了立刻退出，不产生误导性结果。
- **超时控制**：`subprocess.run(..., timeout=N)` 限制单次 ping 的总耗时；`TimeoutExpired` 单独捕获，与"ping 返回非 0（不通）"区分开。
- **日志**：`logging_config.py` 统一配置，`FileHandler` 落盘 + `StreamHandler` 打屏；`logs/` 目录不存在时会自动创建。
- **跨平台**：Windows 的 ping 是 `-n`、输出 GBK，Linux 是 `-c`、输出 UTF-8，代码按 `os.name` 切换，并固定编解码避免乱码。

## 已知限制 / 下一步

- [ ] 串行执行，100 台主机耗时较长，计划改线程池并发
- [ ] 失败时未自动重试，计划加"重试 N 次 + 退避"
- [ ] 只判断"通 / 不通"，尚未从 ping 输出里解析平均延迟与丢包率
- [ ] 退出码固定为 0，接入 cron / 任务计划程序时无法感知失败
- [ ] `timeout` 控制的是进程总耗时，与 ping 自身的 `-w` 无关，两者关系需要重新设计
- [ ] 尚无单元测试

## License

[MIT](LICENSE)



![image-20261118131532974](C:\Users\reall\AppData\Roaming\Typora\typora-user-images\image-20261118131532974.png)

![image-20261118131612791](C:\Users\reall\AppData\Roaming\Typora\typora-user-images\image-20261118131612791.png)
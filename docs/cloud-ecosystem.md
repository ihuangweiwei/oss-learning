# 云平台生态 · 开源项目分析

> **云平台不是黑盒**：阿里云/腾讯云/华为云等底层大量能力都是开源的——本身就是优质开源项目，
> 很多"云上中间件"的社区版就是企业架构的免费底座。本文分析各云厂商生态与云原生基金会的开源项目，
> 映射到 oss-learning 集合内仓库，并给出待引入清单。日期：2026-08-31

## 1. 云厂商开源生态总览

| 云平台 | 代表性开源生态 | 说明 |
|---|---|---|
| **阿里云** | Nacos / Sentinel / RocketMQ / Dubbo / Seata / Spring Cloud Alibaba / Arthas / Canal / Otter / DataX / ChaosBlade / spring-ai-alibaba / ModelScope / Qwen | 国内最完整的中间件开源生态，**大部分已在 java/ 收录** |
| **腾讯云** | Tars（微服务 RPC）、BlueKing（运维平台 bk-ci/bk-cmdb）、TencentKona（JDK）、Angel（ML） | 部分待引入 |
| **华为云** | openGauss（数据库）、openGemini（时序库）、KubeEdge（云边协同）、Volcano（调度）、MindSpore（AI 框架）、openEuler（OS） | 部分待引入 |
| **AWS** | Firecracker（microVM）、Corretto（JDK）、Bottlerocket、Amazon Ion | 偏基础设施，学习价值中等 |
| **微软** | .NET / TypeScript / Semantic Kernel / Copilot 生态 | Semantic Kernel 已在 ai/Framework |
| **云原生基金会 CNCF** | Kubernetes / etcd / Prometheus / Grafana / Envoy / Istio / Argo / containerd / KubeVela | 云原生底座，部分已在集合（grafana 等） |

## 2. 集合内已收录（云生态映射）

| 云生态项目 | 集合内路径 | 归属 |
|---|---|---|
| Nacos（注册/配置中心） | `java/Middleware/nacos`、`java/Manager/nacos*` | 阿里云 |
| Sentinel（流量治理） | `java/Distributed/Sentinel` | 阿里云 |
| RocketMQ（消息） | `java/Middleware/rocketmq*` | 阿里云 |
| Dubbo（RPC） | `java/Distributed/incubator-dubbo`、`java/Spring/dubbo-spring-boot-project`、`java/Go/dubbo-go` | 阿里云 |
| Seata（分布式事务） | `java/Transaction/seata*` | 阿里云 |
| Spring Cloud Alibaba | `java/Spring/spring-cloud-alibaba` | 阿里云 |
| Arthas（诊断） | `java/Manager/arthas` | 阿里云 |
| Canal / Otter（数据同步） | `java/Middleware/canal`、`java/Manager/otter` | 阿里云 |
| spring-ai-alibaba | `ai/Framework/spring-ai-alibaba*` | 阿里云 AI |
| Dapr（云原生运行时） | `java/Platform/dapr` | CNCF/微软 |
| Grafana（可观测） | `java/Middleware/grafana` | CNCF |

## 3. 本期新增（2026-08-31）

| 项目 | 集合内路径 | 云生态归属 | 价值 |
|---|---|---|---|
| etcd | `java/Go/etcd` | CNCF（K8s 核心存储） | 分布式 KV/服务发现底座 |
| KubeEdge | `java/Go/kubeedge` | 华为云（CNCF） | 云边协同，IoT/边缘计算 |
| openGauss | `java/BigData/openGauss` | 华为云 | 企业级关系数据库 |
| openGemini | `java/BigData/openGemini` | 华为云 | 云原生时序数据库（监控/物联网） |
| Tars | `java/Distributed/tars` | 腾讯云 | 微服务 RPC 框架（多语言） |
| ModelScope | `ai/Framework/modelscope` | 阿里云 AI | 模型托管/推理平台，接 DeepSeek/Qwen |

> origin 勘误：openGauss 官方在 `opengauss/openGauss`（非 huaweicloud）；openGemini 在 `openGemini/openGemini`；
> Tars 在 `TarsCloud/Tars`（非 Tencent）。yudao-mall 未单独开源（并入 yudao 主仓，集合已有 yudao-cloud），未引入。

## 4. 待引入候选（按价值排序）

| 项目 | 归属 | 备注 |
|---|---|---|
| Volcengine 生态（字节） | 火山引擎 | 云原生/LLM 编排可研究 |
| BlueKing（bk-cmdb/bk-ci） | 腾讯云 | 运维/CI 平台，较庞大 |
| Volcano | 华为云（CNCF） | K8s 批量调度，AI 训练场景 |
| Istio / Envoy | CNCF | 服务网格（K8s 进阶） |
| KubeVela | 阿里云（CNCF） | 云原生应用交付 |
| PaddlePaddle | 百度 | 深度学习框架（若需中文生态） |

> 引入策略：优先选 **能赋能企业落地 / 是云上服务底座** 的；量级偏大或偏运维的产品（BlueKing 全家桶）按需评估。
> 本分析随技术雷达每轮更新——云厂商新开源的中间件就是下一批"新时代项目"。

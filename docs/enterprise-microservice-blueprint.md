# 企业微服务体系落地蓝图

> 基于 `oss-learning` 仓库集合（java 225 / ai 65 个子模块）整理的一套**可落地的企业微服务参考架构**。
> 每个技术选型都给出本集合内的**对应仓库路径**，用于「学习源码」和「落地选型」两条线。
> 日期：2026-08-31

## 1. 总体分层

```
┌────────────────────────────────────────────────────────────┐
│ 客户端 / 外部流量                                            │
├────────────────────────────────────────────────────────────┤
│ ① 接入层   API 网关 / BFF                                  │
│   higress · shenyu · spring-cloud-gateway · zuul(旧)        │
├────────────────────────────────────────────────────────────┤
│ ② 服务框架   业务服务容器                                   │
│   Spring Boot 3 · Dubbo · quarkus · micronaut · armeria    │
├────────────────────────────────────────────────────────────┤
│ ③ 注册 / 配置中心                                          │
│   Nacos · Apollo · ZooKeeper · disconf(旧)                 │
├────────────────────────────────────────────────────────────┤
│ ④ 服务治理   熔断 / 限流 / 降级                             │
│   Sentinel · Resilience4j · Hystrix(旧)                    │
├────────────────────────────────────────────────────────────┤
│ ⑤ 数据层    分库分表 · 数据同步 · 分布式事务                 │
│   ShardingSphere · dynamic-datasource · canal · Seata      │
├────────────────────────────────────────────────────────────┤
│ ⑥ 基础中间件  缓存 / 消息 / 任务调度                         │
│   Caffeine · Redis · RocketMQ · Pulsar · xxl-job           │
├────────────────────────────────────────────────────────────┤
│ ⑦ 可观测    APM / 监控 / 链路追踪                           │
│   SkyWalking · CAT · Prometheus · Grafana · Sentinel Dash  │
├────────────────────────────────────────────────────────────┤
│ ⑧ 安全认证   SSO / 鉴权 / 网关鉴权                          │
│   Sa-Token · xxl-sso · Spring Security · OAuth2            │
├────────────────────────────────────────────────────────────┤
│ ⑨ 云原生 / 运行时                                          │
│   Dapr · K8s(学习) · Helidon/Quarkus 原生镜像               │
├────────────────────────────────────────────────────────────┤
│ ⑩ AI 赋能层（可选叠加）                                     │
│   Spring AI · LangChain 系 · RAG(Dify/RAGFlow) · Agent     │
└────────────────────────────────────────────────────────────┘
```

## 2. 分层选型 → 仓库映射

> 路径形如 `<super>/<分类>/<仓库名>`。标注 **(生产首选)** 的为当前主流维护项目；标注 **(旧)** 的仅用于理解演进历史。

| 层 | 技术选型 | 对应仓库（oss-learning 内） |
|---|---|---|
| **① 网关** | **Higress**（生产首选） | `ai/Platform/higress` |
| | **Apache ShenYu**（协议转换网关） | `java/Middleware/shenyu` |
| | Spring Cloud Gateway | `java/Spring/*`（spring-cloud 系课程）+ `java/Distributed/gravitee-gateway` |
| | Zuul 1.x（旧，学习用） | `java/Netflix/zuul`、`java/Courses/zuul_lab` |
| **② 服务框架** | **Spring Boot 3**（生产首选） | `java/Spring/spring-boot-examples`、`java/Examples/*`（miaosha、litemall） |
| | **Dubbo 3** | `java/Distributed/incubator-dubbo`（GitHub 重定向=当前 dubbo）、`java/Go/dubbo-go` |
| | Quarkus（K8s/原生镜像） | `java/Framework/quarkus` |
| | Micronaut（Lambda/编译期 DI） | `java/Framework/micronaut-core` |
| | Armeria（异步/多协议） | `java/Framework/armeria` |
| | Helidon（Oracle 轻量） | `java/Framework/helidon` |
| | Vert.x（高并发响应式） | `java/Vertx/*` |
| **③ 注册/配置** | **Nacos**（生产首选） | `java/Middleware/nacos` + `java/Manager/nacos-*`（示例） |
| | Apollo（配置中心） | `java/Courses/apollo_lab` |
| | ZooKeeper（学习） | `java/Distributed/kclient` 等旧分布式组件 |
| **④ 服务治理** | **Sentinel**（生产首选） | `java/Distributed/Sentinel` |
| | Resilience4j（Spring 生态） | `java/Netflix/concurrency-limits`（思想） |
| | Hystrix（旧，学习用） | `java/Netflix/Hystrix`、`java/Courses/hystrix_lab` |
| **⑤ 数据层** | **ShardingSphere**（生产首选） | `java/Distributed/shardingsphere`（官方） + `java/Distributed/sharding-sphere`（旧镜像） |
| | 动态数据源 | `java/Middleware/dynamic-datasource` |
| | 数据同步 | `java/Middleware/canal` |
| | **Seata** 分布式事务 | `java/Transaction/seata` + `java/Transaction/seata-samples` |
| | 分布式 ID | `java/Distributed/tinyid`、`uid-generator`、`vesta-id-generator`（思想）+ xxl 系 |
| **⑥ 基础中间件** | 本地缓存 **Caffeine** | `java/Util/caffeine` |
| | 缓存封装 | `java/Distributed/J2Cache`、`jetcache` |
| | 消息队列 | `java/Middleware/rocketmq`、`pulsar` |
| | **xxl-job** 任务调度（生产首选） | `java/Task/xxl-job` + `xxl-rpc`/`xxl-conf`/`xxl-api` |
| | 旧调度框架（学习） | `java/Task/elastic-job-*`、`Saturn`、`light-task-scheduler` |
| **⑦ 可观测** | **SkyWalking** APM | `java/Distributed/skywalking` |
| | CAT 监控 | `java/Manager/cat` |
| | **Grafana + Prometheus** | `java/Middleware/grafana` + `java/Courses/prom_lab` |
| **⑧ 安全认证** | **Sa-Token**（生产首选） | `java/Framework/Sa-Token` |
| | SSO | `java/Task/xxl-sso`、`java/Courses/oauth2lab` |
| | 权限后台参考 | `java/Manager/*`（zms 等） |
| **⑨ 云原生** | **Dapr**（可移植运行时） | `java/Platform/dapr` |
| | K8s 学习 | `java/Courses/k8s-msa-in-action-ppt` |
| **⑩ AI 赋能** | **Spring AI**（Java 企业 AI） | `java/Spring/spring-ai` + `ai/Framework/spring-ai-alibaba` |
| | Agent 编排 | `ai/Agent/*`、`ai/Framework/langchain/langgraph/semantic-kernel` |
| | RAG 落地 | `ai/RAG/dify`、`ragflow`、`mem0`、`haystack`、`llama_index` |
| | LLM 网关 | `ai/Framework/litellm` |
| | 提示词工程 | `ai/Framework/dspy` |

## 3. 落地路线图（4 阶段）

**Phase 0 · 基建（1–2 周）**
1. 单服务脚手架：Spring Boot 3（参考 `java/Spring/spring-boot-examples`）
2. 引入 Nacos 注册/配置（`java/Middleware/nacos`）
3. 网关：Higress 或 Spring Cloud Gateway

**Phase 1 · 服务化（1–2 月）**
4. RPC 通信：Dubbo 3 或 Feign/OpenFeign（参考 `java/Distributed/incubator-dubbo`）
5. 服务治理：Sentinel 限流熔断（`java/Distributed/Sentinel`）
6. 认证：Sa-Token + xxl-sso（`java/Framework/Sa-Token`）
7. 可观测：SkyWalking + Grafana/Prometheus 全链路

**Phase 2 · 数据与一致性（2–4 月）**
8. 分库分表：ShardingSphere（`java/Distributed/shardingsphere`）
9. 分布式事务：Seata AT/Saga（`java/Transaction/seata` + samples）
10. 任务调度：xxl-job（`java/Task/xxl-job`）
11. 消息解耦：RocketMQ/Pulsar（`java/Middleware/*`）

**Phase 3 · AI 赋能（可选，叠加）**
12. Spring AI + RAG（`java/Spring/spring-ai`、`ai/RAG/dify`）
13. Agent/工作流（`ai/Agent/opencode`、`ai/Agent/crewAI`、`ai/Framework/langgraph`）
14. LLM 统一网关（`ai/Framework/litellm`）

## 4. 学习建议（"先看哪几个"）

- **必读架构**：`java/Examples/miaosha`（秒杀高并发）、`java/Examples/litemall`、`java/Examples/mall-swarm`、`ai/...`（yudao-cloud）
- **核心组件源码**：Nacos、Sentinel、ShardingSphere、Seata、Dubbo、RocketMQ（都在 `java/` 对应分类）
- **微服务课程**：`java/Courses/*_lab`（基于老 Netflix 栈，**看懂思路即可，别抄配置**）

## 5. 淘汰/半淘汰速查（别花时间学）

| 技术 | 替代品 | 对应仓库（保留作历史） |
|---|---|---|
| Eureka / Hystrix / Ribbon / Zuul 1 | Nacos / Sentinel / LoadBalancer / Gateway | `java/Netflix/*`、`java/Courses/*_lab` |
| Cobar / 阿里第一代分库分表 | ShardingSphere | `java/Distributed/cobarclient` 等 |
| disconf / elastic-job / 当当系 | Apollo / xxl-job | `java/Manager/disconf`、`java/Task/elastic-job-*` |
| TCC 老框架 | Seata | `java/Transaction/ByteTCC`、`EasyTransaction` |

## 6. 维护约定

- 本蓝图为**文档型参考**，仓库集合本身不含私有代码；生产落地时按各仓库 LICENSE 合规使用。
- 子模块跟随上游 `latest`（`sync-all.sh`），蓝图中的"生产首选"项会随版本演进，需在落地时复核版本号。

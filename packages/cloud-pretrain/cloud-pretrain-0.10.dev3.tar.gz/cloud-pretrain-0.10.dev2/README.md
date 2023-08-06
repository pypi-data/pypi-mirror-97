
# Cloud Pretrain

CloudPretrain是AI实验室开发的NLP预训练服务框架，集成最新的预训练模型，如BERT, RoBERTa, ALBERT等；通过简单易用的命令行能够快速的选择、训练和部署模型；同时集成了常用的模型训练与推理优化技巧，如混合精度、知识蒸馏、算子优化等。

## 重点功能简介

- **多模型并行训练**
  - 集成了常见的中文预训练模型(`bert-chinese`，`bert-wwm-ext`，`albert`，`roberta`)，并有支持不同大小的模型（3层，6层，12层，24层等）
  - 针对同一个数据集，支持并行实验，快速完成不同中文预训练模型精度对比
- **推理优化**
  - 支持任意基于Bert的checkpoint转换成FP16模型，已经更优的Fast-Transformer格式转换
  - 目前可以支持p99 < <font color=red>**30ms**</font>的情况下，单张T4/V100显卡支撑超过<font color=red>**1500**</font>QPS（seq_len = 16）（bert-base）
  - 低QPS下（< 500），支持更快的推理速度，p99可以降低至20ms以下（bert-base）
- **实验结果展示及记录**
  - 针对一份数据集，支持训练结果展示，测试结果展示等。（目前支持分类任务）
- **发布特定领域适配的预训练模型**
  - 发布了基于小爱领域知识的预训练模型，在相关下游任务上有0.5% ~ 1%的精度提升

相关细节可以浏览[快速上手](docs/quick_start.md)。

## 架构示意图

CloudPretrain一共分为四层：
- [CloudML](http://docs.api.xiaomi.net/cloud-ml/)和[FDS](http://docs.api.xiaomi.net/fds/)：分别是底层的深度学习平台和分布式文件系统平台；
- 功能层：支持模型管理、训练与推理优化、数据管理；功能层以镜像的方式支持模型和优化技巧持续扩展；
- 接口层：支持train/predict/export/serving等模型训练、测试、部署常用命令；
- 应用层：支持分类、(序列标注 todo)等常见NLP任务。

![架构示意图](docs/image/architecture.png)

## 用户支持群

欢迎加入用户支持群，将工具使用中的问题或需求反馈给开发者，感谢！

也可以直接飞书： 赵群，吴晓琳寻求优化支持

![欢迎加入用户支持群](docs/image/feishu.png)


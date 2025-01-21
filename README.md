# AIInteractiveNovel
ai交互式自动小说软件（多大模型协同创作模式）
该软件支持多个ollama 模型同时共同创作一部小说，一个大模型做编辑，一个大模型做作家，你交给每个模型他们的角色后，他们互相合作互相交流，共同输出小说作品

这是个web服务，本地部署，先通过本地部署两个大模型
ollama cp qwen2 qwen2_b

ollama run qwen2

ollama run qwen2_b


那千问来举例，就是这样启动好后，配置代码中的模型相关配置，本地5000端口启动

本服务添加了大模型长期记忆模块，记忆会自动放入本地目录，可以手动删除，保证前后文大模型的思维逻辑一致

输出的小说作品会自动存放到本地

![image](https://github.com/user-attachments/assets/9bb7403d-f7f0-462e-9202-403db740e59a)


# Astrbot 信息查询插件

![AstrbotPlugin-ProfileSearch](https://socialify.git.ci/QingFengTechnology/AstrbotPlugin-ProfileSearch/image?description=1&font=KoHo&language=1&name=1&pattern=Circuit+Board&theme=Auto)

> [!Warning]
> 本插件仅供学习交流，使用者不得用于非法或侵权行为，否则自行承担全部责任。\
> 本插件仅通过 Onebot 协议获取公开信息，插件所有者不对数据的准确性、完整性负责。\
> 不对魔改本插件（如接入社工库等违规操作）的行为负责，违者自行承担法律责任。\
> 使用者应自行评估使用风险，插件所有者不对使用过程中产生的任何损失或风险承担责任。\
> 本声明适用中华人民共和国法律，争议由插件所有者所在地法院管辖。\
> 插件所有者保留对本声明的最终解释权，并有权随时修改。


## 安装

在 Astrbot 应用市场点击右下角 + 号，选择`从链接安装`，复制粘贴本仓库 URL 并点击安装即可。

## 使用

- 自动开盒新群友（需在配置里添加群聊白名单）
- 指令调用：

```plaintext
/box [@目标]
/box [QQ号]
```

![33cd17b7bd27520aee2f463ff8a9d12](https://github.com/user-attachments/assets/97ffe26f-bf18-4cbe-93f4-1eb82e08edeb)

## 配置

```json
{
    "only_admin": {
        "description": "仅bot管理员可开盒他人",
        "type": "bool",
        "hint": "但自己开盒自己不受限制",
        "default": false
    },
    "increase_box": {
        "description": "自动开盒新进群的人",
        "type": "bool",
        "default": false
    },
    "decrease_box": {
        "description": "自动开盒主动退群的人",
        "type": "bool",
        "default": false
    },
    "auto_box_groups": {
        "description": "自动开盒群聊白名单",
        "type": "list",
        "hint": "只自动开盒白名单群聊的新群友/主动退群的人，不填则默认所有群聊都启用自动开盒",
        "default": []
    },
    "box_blacklist": {
        "description": "开盒黑名单",
        "type": "list",
        "hint": "开盒时，会忽略黑名单中的用户，建议将bot自身QQ号写上",
        "default": []
    }
}
```
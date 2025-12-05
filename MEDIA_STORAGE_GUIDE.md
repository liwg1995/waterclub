# 媒体文件存储配置指南

本项目支持多种媒体文件存储方案，包括本地存储和云对象存储服务。系统提供了灵活的配置管理界面，允许管理员在不同存储方案之间切换。

## 目录

- [支持的存储方案](#支持的存储方案)
- [快速开始](#快速开始)
- [后台管理](#后台管理)
- [API接口](#api接口)
- [存储配置详解](#存储配置详解)
- [在文本编辑器中使用](#在文本编辑器中使用)
- [常见问题](#常见问题)

## 支持的存储方案

### 1. 本地存储 (Local)

**适用场景**：开发、测试、小型项目

**优点**：
- 无需额外配置
- 开发调试方便
- 无第三方依赖

**缺点**：
- 不支持分布式部署
- 硬盘容量有限
- 无 CDN 加速

**配置示例**：
```json
{
  "name": "本地存储",
  "storage_type": "local",
  "bucket_name": "",
  "access_url": "http://localhost:8000/media",
  "credentials": {}
}
```

---

### 2. 腾讯云对象存储 (COS)

**适用场景**：中大型项目，需要 CDN 加速

**依赖包**：`cos-python-sdk-v5`

**安装**：
```bash
pip install cos-python-sdk-v5
```

**配置示例**：
```json
{
  "name": "腾讯COS",
  "storage_type": "tencent_cos",
  "bucket_name": "my-bucket-1234567890",
  "access_url": "https://my-bucket-1234567890.cos.ap-beijing.myqcloud.com",
  "credentials": {
    "secret_id": "your-secret-id-here",
    "secret_key": "your-secret-key-here",
    "region": "ap-beijing"
  }
}
```

**获取凭证**：
1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
2. 进入"API 密钥管理"获取 SecretId 和 SecretKey
3. 选择相应的区域 (region)

---

### 3. 阿里云对象存储 (OSS)

**适用场景**：中大型项目，特别是中国大陆

**依赖包**：`oss2`

**安装**：
```bash
pip install oss2
```

**配置示例**：
```json
{
  "name": "阿里OSS",
  "storage_type": "aliyun_oss",
  "bucket_name": "my-bucket",
  "access_url": "https://my-bucket.oss-cn-beijing.aliyuncs.com",
  "credentials": {
    "access_key_id": "your-access-key-id-here",
    "access_key_secret": "your-access-key-secret-here",
    "region": "cn-beijing"
  }
}
```

**获取凭证**：
1. 登录 [阿里云控制台](https://console.aliyun.com/)
2. 进入"RAM 访问控制"创建 AccessKey
3. 选择相应的区域

---

### 4. 七牛云存储

**适用场景**：内容分发，对象存储

**依赖包**：`qiniu`

**安装**：
```bash
pip install qiniu
```

**配置示例**：
```json
{
  "name": "七牛云",
  "storage_type": "qiniu",
  "bucket_name": "my-bucket",
  "access_url": "https://cdn.example.com",
  "credentials": {
    "access_key": "your-access-key-here",
    "secret_key": "your-secret-key-here"
  }
}
```

**获取凭证**：
1. 登录 [七牛云控制台](https://portal.qiniu.com/)
2. 进入"密钥管理"获取 Access Key 和 Secret Key
3. 配置 CDN 加速域名

---

### 5. MinIO 对象存储（开源）

**适用场景**：私有部署、本地数据中心

**依赖包**：`minio`

**安装**：
```bash
pip install minio
```

**配置示例**：
```json
{
  "name": "MinIO",
  "storage_type": "minio",
  "bucket_name": "my-bucket",
  "access_url": "http://minio.example.com:9000",
  "credentials": {
    "access_key": "minioadmin",
    "secret_key": "minioadmin",
    "endpoint": "minio.example.com:9000"
  }
}
```

**部署 MinIO**：
```bash
# Docker 部署
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /minio_data --console-address ":9001"
```

---

## 快速开始

### 步骤 1：创建存储配置

1. 登录后台管理系统：`http://localhost:8000/admin/`
2. 进入"媒体管理" → "存储配置"
3. 点击"添加存储配置"
4. 填写配置信息：
   - **配置名称**：给配置起个名字（如"本地存储"）
   - **存储类型**：选择存储方案
   - **存储桶名称**：对象存储的桶名（本地存储可为空）
   - **访问URL前缀**：文件访问的 URL 前缀
   - **凭证信息**：根据存储类型填写相应的凭证（JSON格式）
   - **是否启用**：只有启用的配置才会被使用
5. 点击"保存"

### 步骤 2：验证配置

配置保存后，系统会自动验证是否能正常连接。如果连接失败，请检查凭证信息。

### 步骤 3：使用配置

- **通过后台上传**：在"媒体管理" → "媒体文件"查看上传的文件
- **通过 API 上传**：使用 `/api/storage/media-files/upload/` 接口
- **在文本编辑器中使用**：编辑文章时可选择上传图片

---

## 后台管理

### 存储配置管理

在后台管理系统中，可以：

1. **查看所有配置**
   - 配置名称
   - 存储类型（彩色标签）
   - 激活状态
   - 存储桶名称
   - 文件数量
   - 修改时间

2. **激活存储配置**
   - 选中一个配置，点击"激活选中的存储配置"
   - 系统会自动禁用其他配置（同一时间只能有一个配置激活）

3. **编辑配置**
   - 点击配置名称进入编辑页面
   - 可修改访问URL、凭证、文件大小限制等

4. **删除配置**
   - 点击"删除"按钮删除不需要的配置
   - 已上传的文件不会被删除

### 媒体文件管理

在"媒体文件"页面可以：

1. **查看所有文件**
   - 文件名称
   - 文件类型（图片、视频、音频、文档等）
   - 文件大小
   - 所属存储配置
   - 访问链接
   - 上传者信息
   - 上传时间

2. **复制文件链接**
   - 点击文件进入详情页
   - 在"快速复制"部分点击"复制"按钮
   - 可获得以下格式的链接：
     - **直接 URL**：用于浏览器访问
     - **HTML 代码**：用于网页嵌入
     - **Markdown 代码**：用于 Markdown 编辑器

3. **删除文件**
   - 选中一个或多个文件，点击"删除选中的媒体文件"
   - 系统会同时删除存储中的文件和数据库记录

---

## API 接口

### 存储配置 API

#### 获取所有配置
```bash
GET /api/storage/storage-configs/
```

**响应示例**：
```json
[
  {
    "id": 1,
    "name": "本地存储",
    "storage_type": "local",
    "storage_type_display": "本地存储",
    "is_active": true,
    "bucket_name": null,
    "access_url": "http://localhost:8000/media",
    "max_file_size": 100,
    "allowed_extensions": "jpg,jpeg,png,gif,bmp,pdf,doc,docx,xls,xlsx,txt,mp4,avi",
    "use_date_path": true,
    "description": "开发测试使用",
    "media_count": 5,
    "created_at": "2025-12-05T12:00:00Z",
    "updated_at": "2025-12-05T12:00:00Z"
  }
]
```

#### 获取激活的配置
```bash
GET /api/storage/storage-configs/active/
```

#### 激活指定配置
```bash
POST /api/storage/storage-configs/{id}/activate/
```

### 媒体文件 API

#### 上传文件
```bash
POST /api/storage/media-files/upload/

Content-Type: multipart/form-data

file: <file>
description: "文件描述（可选）"
```

**请求示例（使用 curl）**：
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -F "file=@image.jpg" \
  -F "description=演出照片" \
  http://localhost:8000/api/storage/media-files/upload/
```

**响应示例**：
```json
{
  "id": 1,
  "file_name": "image.jpg",
  "file_type": "image",
  "file_type_display": "图片",
  "file_size": 1024000,
  "file_size_mb": 1.0,
  "storage_config": 1,
  "storage_config_name": "本地存储",
  "storage_path": "uploads/2025/12/05/image.jpg",
  "access_url": "http://localhost:8000/media/uploads/2025/12/05/image.jpg",
  "uploaded_by": 1,
  "uploaded_by_username": "admin",
  "description": "演出照片",
  "uploaded_at": "2025-12-05T12:00:00Z",
  "updated_at": "2025-12-05T12:00:00Z"
}
```

#### 获取所有文件
```bash
GET /api/storage/media-files/

# 可选参数
?file_type=image          # 按文件类型过滤
&storage_config=1         # 按存储配置过滤
&search=filename          # 按文件名搜索
&ordering=-uploaded_at    # 排序（-表示倒序）
```

#### 获取文件详情
```bash
GET /api/storage/media-files/{id}/
```

#### 复制文件链接
```bash
POST /api/storage/media-files/{id}/copy_url/

# 返回多种格式的链接：
{
  "url": "http://localhost:8000/media/uploads/2025/12/05/image.jpg",
  "html_code": "<img src=\"http://...\" alt=\"image.jpg\" />",
  "markdown_code": "![image.jpg](http://...)"
}
```

#### 删除文件
```bash
DELETE /api/storage/media-files/{id}/delete_file/

# 或通过 REST API 删除
DELETE /api/storage/media-files/{id}/
```

---

## 存储配置详解

### 基本信息

| 字段 | 说明 | 示例 |
|------|------|------|
| 配置名称 | 此配置的标识 | "本地存储" |
| 存储类型 | 选择使用的存储方案 | "local" |
| 是否启用 | 系统使用的存储配置 | true |
| 配置说明 | 配置的描述 | "用于开发测试" |

### 存储配置

| 字段 | 说明 | 示例 |
|------|------|------|
| 存储桶名称 | 云存储的桶名称 | "my-bucket" |
| 访问URL前缀 | 访问文件的基础URL | "https://bucket.oss-cn-beijing.aliyuncs.com" |

### 认证凭证

根据存储类型，需要填写不同的凭证信息（JSON格式）：

**本地存储**：
```json
{}
```

**腾讯COS**：
```json
{
  "secret_id": "AKID...",
  "secret_key": "...",
  "region": "ap-beijing"
}
```

**阿里OSS**：
```json
{
  "access_key_id": "LTAI...",
  "access_key_secret": "...",
  "region": "cn-beijing"
}
```

**七牛云**：
```json
{
  "access_key": "...",
  "secret_key": "..."
}
```

**MinIO**：
```json
{
  "access_key": "minioadmin",
  "secret_key": "minioadmin",
  "endpoint": "minio.example.com:9000"
}
```

### 高级选项

| 字段 | 说明 | 默认值 |
|------|------|--------|
| 最大文件大小(MB) | 单个文件的最大大小 | 100 |
| 允许的文件扩展名 | 允许上传的文件类型 | jpg,jpeg,png,... |
| 自动创建目录 | 是否自动创建存储目录 | true |
| 使用日期路径 | 是否按YYYY/MM/DD组织文件 | true |

---

## 在文本编辑器中使用

### CKEditor 图片上传

当在后台编辑文章时，使用富文本编辑器（CKEditor）时：

1. 点击编辑器中的"图片"按钮
2. 选择"上传文件"标签
3. 点击"选择文件"上传图片
4. 系统会自动上传到当前激活的存储配置
5. 上传完成后，点击"确定"将图片插入编辑器

### 复制外部文件链接

1. 上传文件到媒体存储
2. 在"媒体文件"页面找到该文件
3. 点击进入文件详情页
4. 在"快速复制"部分复制链接
5. 在编辑器中粘贴链接或 HTML 代码

### 支持的格式

- **HTML 代码**：`<img src="..." alt="..." />`
- **Markdown 代码**：`![描述](url)`
- **直接 URL**：用于其他场景

---

## 常见问题

### Q: 如何切换存储配置？

**A**: 进入后台管理 → 媒体管理 → 存储配置，选中新配置并点击"激活选中的存储配置"。之后上传的文件都会存储到新配置中。

### Q: 切换存储配置后，旧文件如何处理？

**A**: 旧文件仍然保存在原配置中，不会自动迁移。建议在切换前导出或备份重要文件。

### Q: 上传文件时出现"文件大小超限"错误？

**A**: 检查存储配置中的"最大文件大小"设置。可在配置页面修改此值。

### Q: 上传文件时出现"不支持的文件类型"错误？

**A**: 检查文件扩展名是否在"允许的文件扩展名"列表中。可联系管理员修改配置。

### Q: 如何在开发环境和生产环境之间切换存储？

**A**: 创建两个存储配置（如"开发存储"和"生产存储"），根据需要激活相应的配置。

### Q: 云存储连接失败怎么办？

**A**: 
1. 检查凭证信息是否正确
2. 检查网络连接是否正常
3. 检查云服务商的防火墙或访问控制设置
4. 查看后台日志获取更详细的错误信息

### Q: 如何实现文件的定期备份？

**A**: 
- 对于本地存储：使用文件系统备份工具备份 `media` 目录
- 对于云存储：大多数云厂商提供日志和备份功能
- 建议定期导出媒体文件列表作为记录

### Q: 是否支持文件版本控制？

**A**: 当前版本不支持，建议使用云存储厂商的版本控制功能（如开启 OSS 版本控制）。

### Q: 如何限制特定用户的上传权限？

**A**: 通过 Django REST Framework 的权限类可以实现。可修改 `storage/views.py` 中的 `permission_classes`。

---

## 性能优化建议

### 1. 使用 CDN 加速

对于云存储，建议配置 CDN 加速：
- 在访问URL前缀中使用 CDN 域名而不是直接的 OSS/COS 域名
- 配置 CDN 缓存策略以提升访问速度

### 2. 文件优化

- **图片**：上传前压缩，建议使用 WebP 格式
- **视频**：使用合适的编码和比特率
- **文档**：PDF 优化以减小文件大小

### 3. 批量上传

对于批量上传，建议：
- 使用 API 接口实现自动化上传脚本
- 利用批量处理降低网络开销
- 考虑使用分片上传处理大文件

### 4. 定期清理

- 删除不需要的临时文件
- 检查有损坏的文件记录
- 定期审查存储成本

---

## 技术支持

如有问题或建议，请：

1. 查看本文档的"常见问题"部分
2. 查看后台管理的帮助文本
3. 检查应用日志：`logs/django.log`
4. 联系技术支持团队

---

## 相关链接

- [Django 文件上传文档](https://docs.djangoproject.com/en/4.2/topics/files/)
- [腾讯COS 文档](https://cloud.tencent.com/document/product/436)
- [阿里OSS 文档](https://help.aliyun.com/product/31815.html)
- [七牛云文档](https://developer.qiniu.com/)
- [MinIO 文档](https://docs.min.io/)

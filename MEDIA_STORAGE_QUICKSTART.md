# 媒体文件存储系统 - 快速入门指南

## 5分钟快速开始

### 第一步：启动应用

```bash
cd /Users/liwugang/学习/qoder-workspace
python manage.py runserver
```

### 第二步：进入后台管理

1. 打开浏览器，访问：`http://localhost:8000/admin/`
2. 用管理员账号登录

### 第三步：创建本地存储配置（推荐新手使用）

1. 进入菜单：**媒体管理** → **存储配置**
2. 点击右上角 **"添加存储配置"** 按钮
3. 填写以下信息：

| 字段 | 填写内容 |
|------|---------|
| 配置名称 | `本地存储` |
| 存储类型 | 选择 `本地存储` |
| 存储桶名称 | 留空 |
| 访问URL前缀 | `http://localhost:8000/media` |
| 凭证信息 | `{}` |
| 最大文件大小(MB) | `100` |
| 允许的文件扩展名 | `jpg,jpeg,png,gif,pdf` |
| 自动创建目录 | ✓ 勾选 |
| 使用日期路径 | ✓ 勾选 |
| 是否启用 | ✓ 勾选 |

4. 点击 **"保存"** 按钮

### 第四步：验证配置

配置保存后，应该能在列表中看到：
- 存储类型显示为蓝色标签 **"本地存储"**
- 状态显示为 **"✓ 启用"**（绿色）
- 文件数量显示为 **"0 个文件"**

---

## 使用本地存储上传文件

### 方法一：通过 API 上传（推荐开发人员）

```bash
# 需要先获取JWT Token

# 1. 获取Token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'

# 返回示例：
# {"access":"eyJ0eXAi...","refresh":"eyJ0eXAi..."}

# 2. 上传文件
curl -X POST http://localhost:8000/api/storage/media-files/upload/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "description=My Image"

# 返回示例：
# {
#   "id": 1,
#   "file_name": "image.jpg",
#   "file_type": "image",
#   "file_size": 1024000,
#   "file_size_mb": 0.98,
#   "access_url": "http://localhost:8000/media/uploads/2024/12/05/image.jpg",
#   "uploaded_at": "2024-12-05T13:15:00Z"
# }
```

### 方法二：通过后台列表查看已上传文件

1. 进入菜单：**媒体管理** → **媒体文件**
2. 可以看到上传的所有文件列表
3. 每个文件可以：
   - 点击 **访问链接** 直接打开文件
   - 点击 **复制** 按钮，复制三种格式的链接
     - URL: `https://...`
     - HTML: `<img src="..." alt="..." />`
     - Markdown: `![...](...)`

---

## 在文本编辑器中使用上传的图片

### CKEditor 中使用

1. 在后台编辑文章时，打开 CKEditor 编辑器
2. 进入"媒体文件"列表，获取图片的访问链接
3. 在 CKEditor 中：
   - 点击 **"插入/编辑图像"** 按钮
   - 在弹出的对话框中，粘贴获取的链接 URL
   - 点击 **"确定"** 插入图片

或者直接粘贴HTML代码：
1. 在 CKEditor 中选择 **"源代码"** 模式
2. 粘贴从媒体文件复制的 HTML 代码
3. 切换回 **"所见即所得"** 模式即可看到图片

---

## 升级到云存储（可选）

### 使用腾讯云 COS

1. **安装依赖**：
```bash
pip install cos-python-sdk-v5
```

2. **在腾讯云获取凭证**：
   - 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
   - 获取 SecretId 和 SecretKey
   - 记下 COS 的 Bucket 名称和区域

3. **在后台创建新的存储配置**：
   - 配置名称：`腾讯COS`
   - 存储类型：`腾讯云对象存储（COS）`
   - 存储桶名称：`my-bucket-1234567890`
   - 访问URL前缀：`https://my-bucket-1234567890.cos.ap-beijing.myqcloud.com`
   - 凭证信息：
   ```json
   {
     "secret_id": "AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
     "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
     "region": "ap-beijing"
   }
   ```
   - 是否启用：✓ 勾选

4. **验证配置**：
   - 配置保存后，系统会验证连接
   - 如果配置正确，应该能正常使用

### 使用阿里云 OSS

1. **安装依赖**：
```bash
pip install oss2
```

2. **在阿里云获取凭证**：
   - 登录 [阿里云控制台](https://console.aliyun.com/)
   - 进入 RAM 访问控制，创建 AccessKey
   - 记下 Bucket 名称和 Region

3. **在后台创建新的存储配置**：
   - 配置名称：`阿里OSS`
   - 存储类型：`阿里云对象存储（OSS）`
   - 存储桶名称：`my-bucket`
   - 访问URL前缀：`https://my-bucket.oss-cn-beijing.aliyuncs.com`
   - 凭证信息：
   ```json
   {
     "access_key_id": "LTAI4xxxxxxxxxxxxxxxxxxx",
     "access_key_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
     "region": "cn-beijing"
   }
   ```
   - 是否启用：✓ 勾选

### 使用七牛云

1. **安装依赖**：
```bash
pip install qiniu
```

2. **在七牛云获取凭证**：
   - 登录 [七牛云控制台](https://portal.qiniu.com/)
   - 进入"密钥管理"获取 Access Key 和 Secret Key
   - 配置 CDN 加速域名

3. **在后台创建新的存储配置**：
   - 配置名称：`七牛云`
   - 存储类型：`七牛云存储`
   - 存储桶名称：`my-bucket`
   - 访问URL前缀：`https://cdn.example.com`
   - 凭证信息：
   ```json
   {
     "access_key": "Fx2Sx_xxxxxxxxxxxxxxxxxxxx",
     "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   }
   ```
   - 是否启用：✓ 勾选

### 使用 MinIO（私有云存储）

1. **安装依赖**：
```bash
pip install minio
```

2. **部署 MinIO**（如未部署）：
```bash
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /minio_data --console-address ":9001"
```

3. **在后台创建新的存储配置**：
   - 配置名称：`MinIO`
   - 存储类型：`MinIO 对象存储`
   - 存储桶名称：`my-bucket`
   - 访问URL前缀：`http://minio.example.com:9000`
   - 凭证信息：
   ```json
   {
     "access_key": "minioadmin",
     "secret_key": "minioadmin",
     "endpoint": "minio.example.com:9000"
   }
   ```
   - 是否启用：✓ 勾选

---

## 常用操作

### 激活不同的存储方案

1. 进入：**媒体管理** → **存储配置**
2. 选择要激活的配置
3. 点击列表页面右上角的操作按钮，选择"激活选中的存储配置"
4. 或者进入配置详情页面，勾选"是否启用"后保存

**注意**：同一时间只有一个配置被激活。激活新配置时，其他配置会自动被禁用。

### 查看已上传的文件

1. 进入：**媒体管理** → **媒体文件**
2. 可以看到所有已上传的文件列表
3. 支持按以下条件过滤：
   - **文件类型**：图片、视频、音频、文档、其他
   - **存储配置**：选择存储在哪个配置中的文件
   - **上传时间**：按月份分组查看

### 复制文件链接

1. 在"媒体文件"列表中找到需要的文件
2. 点击 **访问链接** 可直接打开文件
3. 点击 **复制** 按钮可快速复制三种格式的链接：
   - **URL**：用于直接分享
   - **HTML**：用于在网页中嵌入
   - **Markdown**：用于Markdown文档

### 删除文件

1. 在"媒体文件"列表中选择要删除的文件
2. 点击文件名进入详情页面
3. 点击下方 **"删除"** 按钮
4. 确认删除后，文件会同时从数据库和存储服务中删除

---

## 常见问题排查

### Q: 上传后看不到文件？
**A**: 检查以下几点：
1. 存储配置是否已启用（状态显示为✓）
2. 文件是否超过最大限制（默认100MB）
3. 文件扩展名是否在允许列表中
4. 若使用云存储，检查凭证是否正确

### Q: 文件链接无法访问？
**A**: 
1. 对于本地存储，确保开发服务器正在运行
2. 对于云存储，确保 AccessKey/SecretKey 正确
3. 检查 URL 前缀是否正确配置
4. 检查网络连接和防火墙设置

### Q: 如何修改允许的文件类型？
**A**: 
1. 进入存储配置详情页面
2. 修改 **"允许的文件扩展名"** 字段
3. 多个扩展名用逗号分隔，不包含点
4. 例如：`jpg,png,gif,pdf,doc,docx`

### Q: 如何限制单个文件的大小？
**A**:
1. 进入存储配置详情页面
2. 修改 **"最大文件大小(MB)"** 字段
3. 默认值为 100 MB
4. 保存后立即生效

### Q: 能否同时使用多个存储方案？
**A**: 可以创建多个配置，但同一时间只有一个被激活。如需同时上传到多个位置，可：
1. 依次激活不同的配置上传
2. 或在代码中修改逻辑支持多个后端

---

## API 速查表

### 获取所有存储配置
```bash
GET /api/storage/storage-configs/
Authorization: Bearer YOUR_TOKEN
```

### 获取当前激活的存储配置
```bash
GET /api/storage/storage-configs/active/
Authorization: Bearer YOUR_TOKEN
```

### 激活指定的存储配置
```bash
POST /api/storage/storage-configs/{id}/activate/
Authorization: Bearer YOUR_TOKEN
```

### 获取所有媒体文件
```bash
GET /api/storage/media-files/
Authorization: Bearer YOUR_TOKEN
```

### 上传文件
```bash
POST /api/storage/media-files/upload/
Authorization: Bearer YOUR_TOKEN
Content-Type: multipart/form-data

file: <binary>
description: <optional>
```

### 获取文件详情和访问链接
```bash
GET /api/storage/media-files/{id}/
Authorization: Bearer YOUR_TOKEN
```

### 复制文件访问链接（三种格式）
```bash
POST /api/storage/media-files/{id}/copy_url/
Authorization: Bearer YOUR_TOKEN

返回：
{
  "url": "https://...",
  "html_code": "<img ... />",
  "markdown_code": "![...](...)"
}
```

### 删除文件
```bash
DELETE /api/storage/media-files/{id}/
Authorization: Bearer YOUR_TOKEN
```

---

## 相关文件

- 📄 [MEDIA_STORAGE_GUIDE.md](./MEDIA_STORAGE_GUIDE.md) - 详细的配置和使用指南
- 📄 [MEDIA_STORAGE_IMPLEMENTATION_SUMMARY.md](./MEDIA_STORAGE_IMPLEMENTATION_SUMMARY.md) - 完整的实现总结
- 📄 [README.md](./README.md) - 项目主文档

---

## 获取帮助

如遇到问题，请查看：
1. 本文档的"常见问题"部分
2. [详细使用指南](./MEDIA_STORAGE_GUIDE.md)
3. 后台存储配置页面的"认证凭证"部分有各个存储类型的配置提示

祝您使用愉快！🎉


# 媒体文件存储系统 - 集成测试指南

本文档提供了完整的测试清单，帮助验证媒体文件存储系统的所有功能。

---

## 前置条件

### 环境检查

```bash
# 1. 进入项目目录
cd /Users/liwugang/学习/qoder-workspace

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 检查数据库连接（确保MySQL正在运行）
python manage.py check

# 应该输出：System check identified no issues (0 silenced).
```

### 数据库初始化

```bash
# 如果是首次使用，执行数据库迁移
python manage.py migrate
```

### 启动服务

```bash
# 启动开发服务器
python manage.py runserver

# 应该输出：
# Django version 4.2.x, using settings 'water_cube_studio.settings'
# Starting development server at http://127.0.0.1:8000/
```

---

## 测试清单

### ✅ 后台管理界面测试

#### 1. 验证菜单显示

- [ ] 进入后台：`http://localhost:8000/admin/`
- [ ] 左侧菜单中应显示"**媒体管理**"菜单项
- [ ] 展开菜单，应显示两个子项：
  - [ ] 存储配置
  - [ ] 媒体文件

#### 2. 存储配置界面测试

**进入：媒体管理 → 存储配置**

##### 列表页面

- [ ] 页面正常加载
- [ ] 显示"添加存储配置"按钮
- [ ] 如果列表为空，显示"暂无数据"信息

##### 创建本地存储配置

- [ ] 点击"添加存储配置"按钮
- [ ] 表单正常加载，包含以下字段：
  - [ ] 配置名称
  - [ ] 存储类型（下拉框显示5个选项）
  - [ ] 存储桶名称
  - [ ] 访问URL前缀
  - [ ] 凭证信息
  - [ ] 最大文件大小
  - [ ] 允许的文件扩展名
  - [ ] 自动创建目录
  - [ ] 使用日期路径
  - [ ] 是否启用
  - [ ] 配置说明

填写以下信息：

```
配置名称：本地存储
存储类型：本地存储
存储桶名称：（留空）
访问URL前缀：http://localhost:8000/media
凭证信息：{}
最大文件大小(MB)：100
允许的文件扩展名：jpg,jpeg,png,gif,pdf
自动创建目录：✓
使用日期路径：✓
是否启用：✓
```

- [ ] 点击"保存"按钮成功保存
- [ ] 返回列表页面后，应该看到新创建的配置
- [ ] 配置的存储类型显示为**蓝色**标签，文本为"本地存储"
- [ ] 配置的状态显示为**✓ 启用**（绿色）
- [ ] 文件数量显示为"**0 个文件**"

##### 创建腾讯COS配置（可选）

- [ ] 点击"添加存储配置"按钮
- [ ] 存储类型选择"腾讯云对象存储（COS）"
- [ ] 填写以下信息：

```
配置名称：腾讯COS
存储类型：腾讯云对象存储（COS）
存储桶名称：your-bucket-name
访问URL前缀：https://your-bucket-name.cos.ap-beijing.myqcloud.com
凭证信息：{"secret_id":"xxx","secret_key":"xxx","region":"ap-beijing"}
```

- [ ] 点击"保存"后，配置应显示为**绿色**标签
- [ ] 本地存储配置应自动变为未启用状态

##### 激活不同配置

- [ ] 返回列表页面
- [ ] 选择"本地存储"配置
- [ ] 点击"激活选中的存储配置"操作按钮
- [ ] 刷新页面后，"本地存储"应该显示为启用状态
- [ ] 其他配置应该变为未启用状态
- [ ] 页面应显示成功消息："存储配置已激活"

#### 3. 媒体文件界面测试

**进入：媒体管理 → 媒体文件**

##### 初始状态

- [ ] 列表页面正常加载
- [ ] 应该显示空列表或已上传的文件列表
- [ ] 应该有过滤选项：
  - [ ] 文件类型（图片、视频、音频、文档、其他）
  - [ ] 存储配置
  - [ ] 上传时间（按月份）
- [ ] 应该有搜索框（可按文件名搜索）

##### 列表列

- [ ] 文件名
- [ ] 文件类型（带标签）
- [ ] 文件大小（MB）
- [ ] 存储配置
- [ ] 访问链接（可点击）
- [ ] 上传者
- [ ] 上传时间

---

### ✅ API 测试

#### 1. 获取认证Token

```bash
# 用管理员账号获取Token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'

# 应该返回：
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
# }
```

- [ ] 成功返回 access token 和 refresh token
- [ ] Token 格式正确（JWT 格式）

#### 2. 获取存储配置 API

```bash
# 列出所有存储配置
curl -X GET http://localhost:8000/api/storage/storage-configs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 应该返回配置列表，包含字段：
# id, name, storage_type, storage_type_display, is_active, 
# bucket_name, access_url, media_count, created_at, updated_at
```

- [ ] 请求成功，状态码 200
- [ ] 返回JSON格式的配置列表
- [ ] 列表中显示已创建的"本地存储"配置
- [ ] is_active 字段值为 true

#### 3. 获取激活的存储配置

```bash
curl -X GET http://localhost:8000/api/storage/storage-configs/active/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 应该返回当前激活的配置
```

- [ ] 请求成功，返回激活的存储配置
- [ ] 返回的配置的 is_active 值为 true

#### 4. 上传媒体文件 API

```bash
# 准备一个测试图片文件（例如 test.jpg）
# 上传文件
curl -X POST http://localhost:8000/api/storage/media-files/upload/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test.jpg" \
  -F "description=Test Image"

# 应该返回：
# {
#   "id": 1,
#   "file_name": "test.jpg",
#   "file_type": "image",
#   "file_size": 12345,
#   "file_size_mb": 0.01,
#   "storage_config": 1,
#   "storage_config_name": "本地存储",
#   "storage_path": "uploads/2024/12/05/test.jpg",
#   "access_url": "http://localhost:8000/media/uploads/2024/12/05/test.jpg",
#   "uploaded_by": 1,
#   "uploaded_by_username": "admin",
#   "uploaded_at": "2024-12-05T13:15:00.000Z",
#   "updated_at": "2024-12-05T13:15:00.000Z"
# }
```

- [ ] 请求成功，状态码 201
- [ ] 返回完整的媒体文件信息
- [ ] file_type 自动识别为 "image"
- [ ] storage_path 包含日期路径（YYYY/MM/DD）
- [ ] access_url 正确格式化
- [ ] 文件实际存储在磁盘上
  - 检查路径：`media/uploads/YYYY/MM/DD/filename`

#### 5. 获取媒体文件列表

```bash
curl -X GET http://localhost:8000/api/storage/media-files/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 应该返回上传的文件列表
```

- [ ] 请求成功，返回文件列表
- [ ] 列表中包含刚上传的文件
- [ ] 分页信息正确（默认每页20条）

#### 6. 获取单个文件详情

```bash
# 使用上传返回的 file_id
curl -X GET http://localhost:8000/api/storage/media-files/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

- [ ] 请求成功，返回文件详情
- [ ] 返回的数据与上传时一致

#### 7. 复制访问链接 API

```bash
curl -X POST http://localhost:8000/api/storage/media-files/1/copy_url/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 应该返回：
# {
#   "url": "http://localhost:8000/media/uploads/2024/12/05/test.jpg",
#   "html_code": "<img src=\"http://localhost:8000/media/uploads/2024/12/05/test.jpg\" alt=\"test.jpg\" />",
#   "markdown_code": "![test.jpg](http://localhost:8000/media/uploads/2024/12/05/test.jpg)"
# }
```

- [ ] 请求成功，返回三种格式的链接
- [ ] URL 格式正确
- [ ] HTML 格式包含 img 标签
- [ ] Markdown 格式正确

#### 8. 删除文件 API

```bash
curl -X DELETE http://localhost:8000/api/storage/media-files/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

- [ ] 请求成功，状态码 204（No Content）
- [ ] 文件从数据库中删除
- [ ] 文件从磁盘上删除

---

### ✅ 文件存储功能测试

#### 1. 本地存储功能

- [ ] 上传文件后，检查文件是否存在于：
  - 路径：`media/uploads/YYYY/MM/DD/filename`
  - 例如：`media/uploads/2024/12/05/test.jpg`
- [ ] 文件能通过浏览器直接访问
  - URL：`http://localhost:8000/media/uploads/2024/12/05/test.jpg`
- [ ] 删除数据库记录后，磁盘上的文件也被删除

#### 2. 文件验证功能

- [ ] 上传超过最大大小的文件：
  ```bash
  # 创建 150MB 的测试文件（超过默认100MB限制）
  dd if=/dev/zero of=large_file.bin bs=1M count=150
  
  # 尝试上传
  curl -X POST http://localhost:8000/api/storage/media-files/upload/ \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -F "file=@large_file.bin"
  ```
  - [ ] 应该收到 400 错误："文件大小不能超过 100 MB"

- [ ] 上传不允许的文件类型：
  ```bash
  # 尝试上传 .exe 文件（假设不在允许列表中）
  curl -X POST http://localhost:8000/api/storage/media-files/upload/ \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -F "file=@test.exe"
  ```
  - [ ] 应该收到 400 错误："不支持的文件类型"

#### 3. 文件类型识别

测试不同类型的文件上传：

- [ ] 图片文件（.jpg, .png, .gif）
  - [ ] file_type 应为 "image"
- [ ] PDF 文件
  - [ ] file_type 应为 "document"
- [ ] 视频文件（.mp4, .avi）
  - [ ] file_type 应为 "video"
- [ ] 其他文件
  - [ ] file_type 应为 "other" 或识别的具体类型

---

### ✅ 后台管理交互测试

#### 1. 后台查看上传的文件

- [ ] 进入：媒体管理 → 媒体文件
- [ ] 应该看到刚才上传的文件列表
- [ ] 点击文件名进入详情页面
- [ ] 详情页面显示：
  - [ ] 文件信息
  - [ ] 存储信息
  - [ ] 访问链接（可点击，可以直接打开文件）
  - [ ] 快速复制按钮

#### 2. 复制链接功能

- [ ] 在文件详情页面，查看"快速复制"部分
- [ ] 应该显示一个输入框和"复制"按钮
- [ ] 点击"复制"按钮
- [ ] 应该弹出 alert：**"链接已复制到剪贴板！"**
- [ ] 粘贴到文本编辑器中，链接应该正确

#### 3. 删除文件

- [ ] 在文件详情页面，点击"删除"按钮
- [ ] 确认删除
- [ ] 文件应该从列表中消失
- [ ] 磁盘上的文件也应该被删除

#### 4. 批量删除

- [ ] 返回文件列表
- [ ] 上传至少2个文件
- [ ] 选中多个文件（使用列表上方的复选框）
- [ ] 在"操作"下拉框中选择"删除选中的媒体文件"
- [ ] 确认删除
- [ ] 所有选中的文件应该被删除
- [ ] 显示消息："已删除 X 个媒体文件"

---

### ✅ 多存储配置切换测试

#### 1. 创建第二个配置

- [ ] 创建另一个存储配置（如阿里OSS或七牛云，或创建第二个本地配置）
- [ ] 激活第一个配置，上传文件
- [ ] 激活第二个配置，上传相同的文件

#### 2. 验证文件隔离

- [ ] 在后台"媒体文件"列表，通过"存储配置"过滤
- [ ] 只显示该配置下的文件
- [ ] 不同配置的文件应该存储在各自的位置或账户中

#### 3. 验证激活切换

- [ ] 通过API激活不同的配置：
  ```bash
  curl -X POST http://localhost:8000/api/storage/storage-configs/{id}/activate/ \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```
- [ ] 每次激活一个新配置，其他应自动禁用
- [ ] 上传的文件应该使用当前激活的配置

---

### ✅ 权限和认证测试

#### 1. 未认证访问

```bash
# 不提供token访问API
curl -X GET http://localhost:8000/api/storage/media-files/
```

- [ ] 应该返回 401 错误："Authentication credentials were not provided."

#### 2. 无效Token访问

```bash
curl -X GET http://localhost:8000/api/storage/media-files/ \
  -H "Authorization: Bearer invalid_token_here"
```

- [ ] 应该返回 401 错误

#### 3. 过期Token刷新

```bash
# 获取新的token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"YOUR_REFRESH_TOKEN"}'
```

- [ ] 应该返回新的 access token
- [ ] 使用新token能正常访问API

---

## 性能测试（可选）

### 批量上传测试

```bash
# 创建100个小文件并上传
for i in {1..100}; do
  echo "test content $i" > test_$i.txt
  curl -X POST http://localhost:8000/api/storage/media-files/upload/ \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -F "file=@test_$i.txt"
done
```

- [ ] 所有文件都应该成功上传
- [ ] 数据库应该正常处理100条记录
- [ ] 列表页面加载时间合理（< 2秒）

### 大文件上传测试

```bash
# 创建 50MB 的文件
dd if=/dev/zero of=large_file.bin bs=1M count=50

# 尝试上传（应该成功，因为在100MB限制内）
curl -X POST http://localhost:8000/api/storage/media-files/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@large_file.bin"
```

- [ ] 上传应该成功
- [ ] 上传时间合理（取决于网络）
- [ ] 文件完整性无损

---

## 故障排查

### 常见问题

#### 数据库连接失败
```
Error: Can't connect to MySQL server on 'localhost'
```
**解决**：
- [ ] 检查MySQL服务是否运行
- [ ] 检查 .env 文件中的数据库配置
- [ ] 确认数据库存在

#### 迁移失败
```
Error: No such table: storage_storageconfig
```
**解决**：
- [ ] 执行迁移：`python manage.py migrate storage`
- [ ] 或执行所有迁移：`python manage.py migrate`

#### 文件上传失败
```
Error: 'StorageConfig' object is not iterable
```
**解决**：
- [ ] 确认至少创建了一个激活的存储配置
- [ ] 检查配置是否正确保存

#### API 返回 403 错误
```
Error: You do not have permission to perform this action.
```
**解决**：
- [ ] 确认使用了有效的token
- [ ] 确认token未过期
- [ ] 查看用户的权限设置

---

## 测试完成清单

### 后台管理
- [ ] 菜单显示正常
- [ ] 存储配置 CRUD 操作正常
- [ ] 媒体文件列表显示正常
- [ ] 文件详情页面正常
- [ ] 链接复制功能正常

### API
- [ ] 认证 API 正常
- [ ] 存储配置 API 正常
- [ ] 媒体文件上传 API 正常
- [ ] 媒体文件列表 API 正常
- [ ] 文件删除 API 正常
- [ ] 链接复制 API 正常

### 功能
- [ ] 文件上传正常
- [ ] 文件存储正常
- [ ] 文件验证正常
- [ ] 文件类型识别正常
- [ ] 文件删除正常
- [ ] 配置切换正常

### 安全性
- [ ] 认证要求正常
- [ ] 权限控制正常
- [ ] Token 刷新正常

---

## 测试报告

填写以下内容生成测试报告：

```
测试日期：YYYY-MM-DD
测试人员：Your Name
Django 版本：4.2.x
Python 版本：3.x.x
数据库：MySQL x.x

总测试项：XX
通过：XX
失败：XX
跳过：XX

问题记录：
（如有失败项，在此记录）

备注：
```

---

## 相关文档

- [MEDIA_STORAGE_GUIDE.md](./MEDIA_STORAGE_GUIDE.md) - 详细配置指南
- [MEDIA_STORAGE_QUICKSTART.md](./MEDIA_STORAGE_QUICKSTART.md) - 快速入门
- [MEDIA_STORAGE_IMPLEMENTATION_SUMMARY.md](./MEDIA_STORAGE_IMPLEMENTATION_SUMMARY.md) - 实现总结

---

祝测试顺利！🧪


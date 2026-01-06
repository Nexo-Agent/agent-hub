# Đề xuất Specialist Agents cho Nexo Hub

Dựa trên tài liệu BRD v1.0, dưới đây là 3 Specialist Agents được đề xuất để khởi tạo hệ sinh thái. Các agent này tập trung vào các use-case cốt lõi của lập trình viên: Chất lượng code, Tài liệu, và Thử nghiệm nhanh.

---

## 1. Code Warden (Người Giám Hộ Code)

Chuyên gia về Clean Code, Security và Best Practices.

- **Manifest ID:** `com.nexo.codewarden`
- **Tên hiển thị:** Code Warden
- **Routing Trigger:** `@audit`, `@review`, `@check`
- **Mô tả:** Phân tích code tĩnh để tìm lỗi logic, lỗ hổng bảo mật và đề xuất tối ưu hóa (Refactor).

### Cấu trúc Gói

```text
codewarden-v1/
├── manifest.yaml
├── instructions/
│   └── persona.md       # "Bạn là Senior Software Architect, cực kỳ khó tính về clean code..."
└── tools/
    ├── main.py
    └── linters.py       # Wrapper cho Pylint, ESLint, Bandit
```

### Capability (Python Tools)

1.  **`scan_file(path)`**: Chạy linter (flake8/eslint) trả về danh sách warning/error.
2.  **`security_check(path)`**: Quét các pattern nguy hiểm (hardcoded credentials, SQL injection).
3.  **`complexity_score(path)`**: Tính độ phức tạp Cyclomatic.

---

## 2. DocuSmith (Thợ Dữ Liệu)

Chuyên gia viết tài liệu kỹ thuật và release notes.

- **Manifest ID:** `com.nexo.docusmith`
- **Tên hiển thị:** DocuSmith
- **Routing Trigger:** `@docs`, `@write`
- **Mô tả:** Tự động đọc mã nguồn và sinh ra JSDoc, Docstring, README.md hoặc Release Notes từ git diff.

### Cấu trúc Gói

```text
docusmith-v1/
├── manifest.yaml
├── instructions/
│   └── persona.md       # "Bạn là Technical Writer chuyên nghiệp tại Google..."
└── tools/
    ├── main.py
    └── parser.py        # Phân tích cây cú pháp (AST) để hiểu hàm/class
```

### Capability (Python Tools)

1.  **`read_structure(path)`**: Trả về outline của file (tên hàm, tham số) để LLM không cần đọc raw file quá dài.
2.  **`generate_markdown(content)`**: Tool định dạng output markdown chuẩn đẹp.
3.  **`git_diff_summary(commits)`**: Tóm tắt thay đổi từ git log để viết Changelog.

---

## 3. PyRunner (Môi trường Thực thi)

Chuyên gia chạy script và xử lý dữ liệu nhanh.

- **Manifest ID:** `com.nexo.pyrunner`
- **Tên hiển thị:** PyRunner
- **Routing Trigger:** `@run`, `@calc`, `@data`
- **Mô tả:** Một môi trường Python Sandbox an toàn để User nhờ viết và chạy các script xử lý dữ liệu nhỏ, vẽ biểu đồ, hoặc test logic nhanh.

### Cấu trúc Gói

```text
pyrunner-v1/
├── manifest.yaml
├── instructions/
│   └── persona.md       # "Bạn là Data Scientist, hãy viết code python để giải quyết vấn đề..."
└── tools/
    ├── main.py
    └── repl.py          # Jupyter-like execution environment
```

### Capability (Python Tools)

1.  **`execute_python(code)`**: Chạy code Python trong isolated process và trả về stdout/stderr.
2.  **`install_package(name)`**: (Optional) Cài nhanh thư viện cần thiết vào venv tạm thời.
3.  **`plot_data(data)`**: Sinh ảnh biểu đồ (matplotlib) và trả về đường dẫn file ảnh.

---

# Tier 2: Advanced Agents (High Complexity)

Đây là các agent có khả năng thực hiện chuỗi tác vụ phức tạp (Autonomous Loops), sử dụng nhiều công cụ phối hợp và có thể thay đổi trạng thái hệ thống.

## 4. The Builder (Kỹ Sư Full-Stack)

Chuyên gia thực thi tính năng: Đọc code -> Lập kế hoạch -> Viết code -> Chạy test -> Fix lỗi.

- **Manifest ID:** `com.nexo.builder`
- **Routing Trigger:** `@builder`, `@implement`, `@refactor`
- **Complexity:** High (Read/Write Filesystem + Terminal Execution)

### Cấu trúc Toolset (`tools/`)

Agent này sở hữu bộ công cụ tương tự như một IDE backend:

1.  **`file_system`**:
    - `search_code(query)`: Grep thông minh tìm vị trí cần sửa.
    - `read_file(path)`: Đọc nội dung file.
    - `edit_file(path, diff)`: Patch nội dung file cẩn trọng.
2.  **`terminal`**:
    - `run_command(cmd)`: Chạy lệnh build, test (vd: `npm test`, `cargo build`).
    - `read_stdout(pid)`: Đọc kết quả log dài.
3.  **`planner`**:
    - `create_plan(steps)`: Lưu trạng thái kế hoạch vào memory để không bị lạc hướng khi gặp lỗi.

### Example Workflow

1.  User: `@builder thêm tính năng login bằng Google`
2.  Builder:
    - `file_system.search("auth")` -> Tìm thấy `auth_service.ts`.
    - `file_system.read(...)` -> Hiểu cấu trúc hiện tại.
    - `planner.create(...)` -> Lên plan 3 bước (Install SDK, Config Route, UI Button).
    - `terminal.run("npm install firebase-admin")`.
    - `file_system.edit(...)` -> Sửa code.
    - `terminal.run("npm run test")` -> **FAIL**.
    - **Self-Correction**: Đọc lỗi -> Sửa lại code -> Test lại -> **PASS**.
3.  Builder: "Đã hoàn thành. Đã chạy test success."

---

## 5. Cloud Commander (DevOps & Infra)

Chuyên gia quản trị hạ tầng, Docker và Kubernetes.

- **Manifest ID:** `com.nexo.ops`
- **Routing Trigger:** `@ops`, `@deploy`, `@status`
- **Complexity:** High (External API Interaction + State Management)

### Cấu trúc Toolset

1.  **`docker_client`**: (Wrapper quanh Docker SDK)
    - `list_containers()`, `get_logs(container_id)`, `restart_container(id)`.
    - `build_image(tag)`, `prune_system()`.
2.  **`k8s_client`** (Optional):
    - `kubectl_apply(manifest)`, `get_pods()`.
3.  **`network_utils`**:
    - `curl_check(url)`: Ping healthcheck services.
    - `port_scan(host)`: Kiểm tra port mở.

### Example Workflow

1.  User: `@ops server api đang lỗi 500, check giúp tôi`
2.  Ops:
    - `docker_client.list_containers()` -> Thấy container `api-server` đang chạy.
    - `docker_client.get_logs("api-server", tail=50)` -> Thấy lỗi "Connection refused to Database".
    - `network_utils.curl_check("postgres:5432")` -> **Timeout**.
    - Suy luận: Database bị treo hoặc mất mạng.
    - `docker_client.restart_container("postgres")`.
    - `network_utils.curl_check(...)` -> **OK 200**.
    - `network_utils.curl_check("api-server")` -> **OK 200**.
3.  Ops: "Database bị treo, tôi đã restart và hệ thống đã hoạt động lại."

---

## 6. QA Auto-Pilot (Kiểm thử Tự động)

Chuyên gia kiểm thử End-to-End, điều khiển trình duyệt thực.

- **Manifest ID:** `com.nexo.qa`
- **Routing Trigger:** `@qa`, `@test-ui`, `@verify`
- **Complexity:** Very High (Browser Control + Visual Verification)

### Cấu trúc Toolset

1.  **`browser_controller`** (Sử dụng Playwright/Selenium Driver):
    - `navigate(url)`, `click(selector)`, `type(selector, text)`.
    - `screenshot(path)`: Chụp ảnh màn hình làm bằng chứng.
    - `get_dom_snapshot()`: Đọc cấu trúc HTML hiện tại.
2.  **`visual_diff`**:
    - `compare_images(img1, img2)`: So sánh giao diện trước/sau khi đổi design.
3.  **`report_gen`**:
    - `create_test_report(json)`: Xuất báo cáo HTML đẹp.

### Example Workflow

1.  User: `@qa verify trang đăng ký user mới`
2.  QA:
    - `browser_controller.navigate("localhost:3000/signup")`.
    - `browser_controller.type("#email", "test@nexo.ai")`.
    - `browser_controller.click("#submit")`.
    - `browser_controller.wait_for_selector(".welcome-message")` -> **Timeout** (Không thấy lời chào).
    - `browser_controller.screenshot("error_signup.png")`.
    - `browser_controller.get_dom_snapshot()` -> Thấy có lỗi validation đỏ rực "Password too weak".
3.  QA: "Test Failed. Form yêu cầu mật khẩu mạnh nhưng tôi chưa nhập. Xem ảnh: `error_signup.png`."

---

## Tổng kết kỹ thuật (Updated)

Với yêu cầu "Phức tạp & Nhiều Tool", nhóm Tier 2 này đòi hỏi:

1.  **Multi-step Reasoning (Suy luận đa bước)**: Agent phải tự biết gọi tool kiểm tra trước khi gọi tool sửa lỗi.
2.  **Environment Feedback**: Agent phải biết đọc kết quả từ terminal/browser để biết mình làm đúng hay sai.
3.  **State Persistence**: Phải nhớ được plan ban đầu để tránh đi vào vòng lặp vô tận.

Lời khuyên: Để triển khai nhóm này, bạn cần integrate một thư viện agentic workflow (như LangGraph hoặc AutoGen) vào trong `main.py` của mỗi gói.

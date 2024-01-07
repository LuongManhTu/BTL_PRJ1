-------- Phần mềm vẽ đồ thị và mô phỏng thuật toán DFS, BFS trên đồ thị -------------


*** Các thành phần trên giao diện và các thao tác với chúng ***

  -  Canvas: Khu vực hiển thị đồ thị, góc phải bên dưới có Navigation bar để thao tác thu phóng, dịch chuyển đồ thị.
  
  -  Radio button Undirected Graph / Directed Graph: Chọn loại đồ thị vô hướng / có hướng.
  
  -  Các nút chỉnh sửa đồ thị và input box tương ứng, khi ấn sẽ hiển thị ngay kết quả trên Canvas:
      + Add vertex: Thêm đỉnh mới
      + Remove vertex: Xóa đỉnh
      + Add edge: Thêm cạnh mới
      + Remove edge: Xóa cạnh
      (Ví dụ input: Vertex: 6, Edge: 3 4)
      
  -  Input Textarea hiển thị dữ liệu của đồ thị có dạng:
      + Dòng đầu là số đỉnh và cạnh của đồ thị: <số đỉnh> <số cạnh>
      + Các dòng tiếp theo là các cặp đỉnh ứng với các cạnh của đồ thị: <đỉnh u> <đỉnh v>
   
  -  Nút Import Graph: Import dữ liệu đồ thị từ file .txt bất kỳ (đúng dạng trên) vào Input Textarea.

          // Người dùng có thể tạo đồ thị bằng cách thêm thủ công các đỉnh, cạnh bằng nhóm nút chỉnh sửa đồ thị hoặc Import từ file .txt có sẵn.
     
  -  Nút Create Graph: Tạo đồ thị với dữ liệu từ Input Textarea và vẽ trên Canvas.

  -  Input box nhập Start vertex và Target vertex: Nhập đỉnh bắt đầu và đỉnh đích.
      + Nếu để trống Start vertex: Mặc định Start Vertex là nút có chỉ số nhỏ nhất của đồ thị.
      + Nếu để trống Target Vertex: Trở thành thuật toán duyệt đồ thị từ đỉnh bắt đầu (Start vertex)
      + Nếu điền Target vertex: Trờ thành thuật toán tìm đường trên đồ thị từ đỉnh bắt đầu (Start vertex) tới đỉnh đích (Target vertex)

  -  Hai nút DFS, BFS: chạy thuật toán DFS hoặc BFS trên đồ thị đã vẽ.

  -  Output Textarea: Hiển thị trạng thái stack / queue khi duyệt đồ thị bằng thuật toán tương ứng.


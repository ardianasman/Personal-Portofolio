<h1>Students Paper Storage</h1>

How to run :

1. nameko run user
2. nameko run gateway
3. check in postman

Fungsi - fungsi yang ada :
1. /login - Untuk melakukan login agar dapat melakukan fitur yang membutuhkan login
2. /register - Untuk dapat memiliki login dan melakukan fitur yang mebutuhkan login
3. /logout - Untuk menghapus session setelah melakukan login
4. /upload_files - Untuk mengupload file ke localhost akan masuk ke folder "Files"
5. /download_file/<string:x> - Untuk menampilkan data file kedalam response, x sebagai nama file lengkap dengan extension file
{
    "image_directory": "/path/to/images",
    "ftp_details": {
        "host": "ftp.example.com",
        "user": "ftp_user",
        "password": "ftp_password",
        "remote_directory": "/path/to/upload" // Удалённая папка для загрузки
    },
    "photographer_name": "John Doe",
    "log_file": "/path/to/logfile.log"
}

Пример конфигурации для FTP-серверов с пустой или корневой папкой
{
  "ftp_details": [
    {
      "host": "ftp1.example.com",
      "user": "user1",
      "password": "password1",
      "remote_directory": ""  // Пустая строка указывает на корневую директорию
    },
    {
      "host": "ftp2.example.com",
      "user": "user2",
      "password": "password2",
      "remote_directory": "/"  // '/' также указывает на корневую директорию
    }
  ]
}


# Database Schema

## users

| Column     | Type      | Constraints |
|------------|-----------|-------------|
| id         | INTEGER   | PRIMARY KEY |
| email      | VARCHAR   | UNIQUE, NOT NULL |
| is_active  | BOOLEAN   | DEFAULT true |
| created_at | TIMESTAMP | DEFAULT now() |

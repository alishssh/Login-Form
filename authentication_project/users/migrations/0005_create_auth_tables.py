from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_registereduser'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS auth_group (
                id serial PRIMARY KEY,
                name varchar(150) NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS auth_group_permissions (
                id serial PRIMARY KEY,
                group_id integer NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
                permission_id integer NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
                UNIQUE(group_id, permission_id)
            );

            CREATE TABLE IF NOT EXISTS auth_permission (
                id serial PRIMARY KEY,
                name varchar(255) NOT NULL,
                content_type_id integer NOT NULL REFERENCES django_content_type(id) ON DELETE CASCADE,
                codename varchar(100) NOT NULL,
                UNIQUE(content_type_id, codename)
            );

            CREATE TABLE IF NOT EXISTS auth_user (
                id serial PRIMARY KEY,
                password varchar(128) NOT NULL,
                last_login timestamp with time zone,
                is_superuser boolean NOT NULL,
                username varchar(150) NOT NULL UNIQUE,
                first_name varchar(150) NOT NULL,
                last_name varchar(150) NOT NULL,
                email varchar(254) NOT NULL,
                is_staff boolean NOT NULL,
                is_active boolean NOT NULL,
                date_joined timestamp with time zone NOT NULL
            );

            CREATE TABLE IF NOT EXISTS auth_user_groups (
                id serial PRIMARY KEY,
                user_id integer NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                group_id integer NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
                UNIQUE(user_id, group_id)
            );

            CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
                id serial PRIMARY KEY,
                user_id integer NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                permission_id integer NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
                UNIQUE(user_id, permission_id)
            );
        """)
    ] 
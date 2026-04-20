-- =============================================
-- Proyecto: Data Cleaning Pipeline - Agentes WFM
-- Script de Transformación y Carga
-- =============================================

-- 1. Limpieza de la tabla destino antes de la carga (Opcional, para evitar duplicados al re-ejecutar)
TRUNCATE TABLE [CleanData#2];

-- 2. Proceso de limpieza y carga masiva
WITH DataProcesada AS (
    SELECT
        id,
        -- Limpieza de Nombre: Quita espacios y maneja vacíos
        COALESCE(NULLIF(TRIM(nombre),''), 'Not_Found') AS nombre,

        -- Validación de Edad: Rango laboral (18-65 años)
        CASE	
            WHEN TRY_CAST(edad AS INT) BETWEEN 18 AND 65
                THEN TRY_CAST(edad AS INT)
            ELSE NULL
        END AS edad,

        -- Validación de Correo: Patrón básico y minúsculas
        CASE	
            WHEN correo LIKE '%_@_%_._%' 
                THEN LOWER(TRIM(correo))
            ELSE 'NA'
        END AS correo,

        -- Limpieza de Teléfono: Quita guiones y valida que sea numérico
        CASE
            WHEN REPLACE(telefono, '-','') NOT LIKE '%[^0-9]%' 
                THEN REPLACE(telefono,'-','')
            ELSE NULL
        END AS telefono,

        -- Formato de Ciudad: Primera letra Mayúscula
        CASE 
            WHEN ciudad IS NOT NULL 
                THEN UPPER(LEFT(TRIM(ciudad),1)) + LOWER(SUBSTRING(TRIM(ciudad), 2, LEN(ciudad)))
            ELSE NULL
        END AS ciudad,

        -- Normalización de Fecha: Maneja múltiples formatos
        COALESCE( 
            TRY_CAST(fecha_ingreso AS DATE),
            TRY_CONVERT(DATE, fecha_ingreso, 103),
            TRY_CONVERT(DATE, fecha_ingreso, 105)
        ) AS fecha_ingreso,

        -- Limpieza de Salario: Conversión a Decimal(10,2)
        CASE 
            WHEN TRY_CAST(salario AS DECIMAL(10,2)) > 0
                THEN TRY_CAST(salario AS DECIMAL(10,2))
            ELSE NULL
        END AS salario
    FROM dbo.Agentes
)
-- 3. Inserción en la tabla destino
INSERT INTO [CleanData#2]
SELECT * FROM DataProcesada
WHERE fecha_ingreso IS NOT NULL; -- Filtro de seguridad para fechas

-- 4. Verificación rápida
SELECT * FROM [CleanData#2];

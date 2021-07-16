


-- =============================================
-- Author:		<Helmut Eggert>
-- Create date: <18.03.2015>
-- Description:	<Prozedur um ein bestehendes Paket mit allen zugehörigen Paketelementen und Kalkulationen in eine Konfiguration einzufügen>
--				<Eingabewerte sind die ID der zu ergänzenden Konfiguration, die ID des einzufügenden Pakets und die ID des Users der die Prozedur aufruft. Filtereinstellungen werden übernommen>
-- =============================================
CREATE PROCEDURE [dbo].[SP_NAV_INSERT_PACKAGE_WITH_FILTER]

	@N_ID INT,
	@NP_ID INT,
	@USER_ID INT

AS
    DECLARE @NP_ID_NEW INT
    DECLARE @NPE_ID_NEW INT
    DECLARE @NPE_ID INT
    DECLARE @DM_ID INT
    DECLARE @NL_ID INT
    DECLARE @ZM_LOCATION nvarchar (5)
    DECLARE @NPE_CREATE BIT
	DECLARE @NPE_CREATE_SO BIT
    DECLARE @CT_ID INT
    DECLARE @MyError INT


BEGIN

SET @MyError = 0

	-- <Prüfen ob N_ID und NP_ID vorhanden>
	IF EXISTS (SELECT N_ID FROM NAV WHERE (N_ID = @N_ID)) AND EXISTS (SELECT NP_ID FROM NAV_PACK WHERE (NP_ID = @NP_ID))
	BEGIN
	BEGIN TRANSACTION INSERT_PACKAGE
		-- <NAV_PACK duplizieren>
		INSERT INTO dbo.NAV_PACK (N_ID, NP_NAME_DE, NP_NAME_EN, NP_COMMENT_DE, NP_COMMENT_EN, CL_ID, NP_CLEARDATE, NP_CLEARBY, ZM_PRODUCT, PT_ID, NP_TESTSAMPLES, NP_IS_TEMPLATE, NP_TEMPLATE_ID, PN_ID, NP_REG, NP_REGBY)
			SELECT @N_ID, NP_NAME_DE, NP_NAME_EN, NP_COMMENT_DE, NP_COMMENT_EN, CL_ID, NP_CLEARDATE, NP_CLEARBY, ZM_PRODUCT, PT_ID, NP_TESTSAMPLES, 0, @NP_ID, PN_ID, GETDATE(), @USER_ID
			FROM dbo.NAV_PACK
			WHERE NP_ID = @NP_ID
			SET @MyError = @MyError + @@ERROR
		SET @NP_ID_NEW = @@IDENTITY

		-- <NAV_PACK_SERVICECLASS duplizieren>
		INSERT INTO dbo.NAV_PACK_SERVICECLASS
                      (NP_ID, SCL_ID)
			SELECT @NP_ID_NEW, SCL_ID
			FROM dbo.NAV_PACK_SERVICECLASS
			WHERE (NP_ID = @NP_ID)
			SET @MyError = @MyError + @@ERROR

		-- <NAV_PACK_ELEMENT duplizieren>

		-- Cursor deklarieren
		DECLARE	MY_CURSOR CURSOR FOR

		-- die zu durchlaufenden Datensätze bestimmen
			SELECT NPE_ID, DM_ID, NL_ID, ZM_LOCATION, CT_ID, NPE_CREATE, NPE_CREATE_SO
			FROM dbo.NAV_PACK_ELEMENT
			WHERE (NP_ID = @NP_ID)

		-- Cursor öffnen und erste Ergebniszeile in die Hilfsvariablen einlesen
		OPEN MY_CURSOR
		FETCH NEXT FROM MY_CURSOR INTO @NPE_ID, @DM_ID, @NL_ID, @ZM_LOCATION, @CT_ID, @NPE_CREATE, @NPE_CREATE_SO
		-- Schleife, bis keine Ergebniszeile mehr übrig ist
		WHILE @@FETCH_STATUS = 0
		BEGIN

			-- NAV_PACK_ELEMENT kopieren
			INSERT INTO dbo.NAV_PACK_ELEMENT (NP_ID, DM_ID, NL_ID, ZM_LOCATION, CT_ID, NPE_CREATE, NPE_CREATE_SO, NPE_REG, NPE_REGBY)
			VALUES (@NP_ID_NEW, @DM_ID, @NL_ID, @ZM_LOCATION, @CT_ID, @NPE_CREATE, @NPE_CREATE_SO, GETDATE(), @USER_ID)
			SET @MyError = @MyError + @@ERROR
			SET @NPE_ID_NEW =  @@IDENTITY

			-- NAV_PACK_ELEMENT_CALC kopieren
			INSERT INTO dbo.NAV_PACK_ELEMENT_CALC
                      (NPE_ID, ST_ID, NPEC_DELTA_START, NPEC_TIME_DAYS, NPEC_TIME_HOURS, NPEC_RATE, NPEC_COSTS, NPEC_TRAVEL, NPEC_FACTOR, NPEC_PRICE,
                      NPEC_COMMENT, NPEC_TASK, ZM_ID, NPOS_ID, NPEC_REG, NPEC_REGBY)
            SELECT @NPE_ID_NEW, ST_ID, NPEC_DELTA_START, NPEC_TIME_DAYS, NPEC_TIME_HOURS, NPEC_RATE, NPEC_COSTS, NPEC_TRAVEL, NPEC_FACTOR, NPEC_PRICE,
                      NPEC_COMMENT, NPEC_TASK, ZM_ID, NPOS_ID, GETDATE(), @USER_ID
            FROM NAV_PACK_ELEMENT_CALC
            WHERE (NPE_ID = @NPE_ID)
            SET @MyError = @MyError + @@ERROR

			-- NAV_PACK_ELEMENT_PROOF kopieren
            INSERT INTO dbo.NAV_PACK_ELEMENT_PROOF
            (NPE_ID, NPEP_TYPE, NPR_ID, NPEP_TEXT_DE, NPEP_TEXT_EN, NPEP_REG, NPEP_REGBY)
            SELECT @NPE_ID_NEW, NPEP_TYPE, NPR_ID, NPEP_TEXT_DE, NPEP_TEXT_EN, GETDATE(), @USER_ID
            FROM NAV_PACK_ELEMENT_PROOF
            WHERE (NPE_ID = @NPE_ID)
            SET @MyError = @MyError + @@ERROR

			-- NAV_PACK_ELEMENT_FILTER kopieren
            INSERT INTO dbo.NAV_PACK_ELEMENT_FILTER
			(NPE_ID, DMI_ID, NPEF_REG, NPEF_REGBY)
            SELECT @NPE_ID_NEW, DMI_ID, GETDATE(), @USER_ID
            FROM NAV_PACK_ELEMENT_FILTER
            WHERE (NPE_ID = @NPE_ID)
            SET @MyError = @MyError + @@ERROR

			-- die nächste Ergebniszeile in die Hilfsvariablen einlesen
			FETCH NEXT FROM MY_CURSOR INTO @NPE_ID, @DM_ID, @NL_ID, @ZM_LOCATION, @CT_ID, @NPE_CREATE, @NPE_CREATE_SO

		END

		-- Cursor schließen und Speicher freigeben
		CLOSE MY_CURSOR
		DEALLOCATE MY_CURSOR
	IF @MyError = 0
		BEGIN
		COMMIT TRANSACTION INSERT_PACKAGE
		END
	ELSE
		BEGIN
		PRINT @MyError
		ROLLBACK TRANSACTION INSERT_PACKAGE
		END
	END
END

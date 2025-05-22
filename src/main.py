import config
import core
import data



if __name__ == "__main__":

	settings = config.Settings()
	# data.mediator.create_file(settings.DATA_STORAGE_URL.get_secret_value() + "/test.metafile", "Some test information", "{}")
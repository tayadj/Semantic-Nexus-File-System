import config
import core



if __name__ == "__main__":

	settings = config.Settings()
	engine = core.Engine(settings)
	manager = core.Manager(settings)

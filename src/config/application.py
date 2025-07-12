import fastapi
import uvicorn



class Application:

	def __init__(self, engine, settings):

		self.application = fastapi.FastAPI()

		uvicorn.run(self.application, host = "localhost", port = 8000)

	def setup(self):

		@self.application.get("/health")
		def health(self):

			return {
				"status": "OK"
			}
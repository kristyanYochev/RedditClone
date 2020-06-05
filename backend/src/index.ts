import * as express from "express";
import { Request, Response } from "express";
import { config as envConfig } from "dotenv";

envConfig();

const port = process.env.PORT || 3000;
const app = express();

app.get("/", async (req: Request, res: Response, next: Function) => {
  res.send("Hello World");
});

app.listen(port, () => {
  console.log(`Server listening on ${port}`);
});

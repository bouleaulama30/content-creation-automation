const express = require('express')
const { exec } = require('child_process');

const shell = require('shelljs')
const app = express()
app.use(express.json())


app.get("/api", (req, res) => {
    res.json({"users": ["user10", "user2", "user3"]})
    console.log("get /api bien reçu")
})

app.post("/test", (req, res) => {
    const link = req.body.link;
    const template = req.body.template;
    shell.exec(`../../automate.sh ${template}`)
    // console.log(req.body);
})

app.listen(5000, () => {console.log("Server started on port 5000")})
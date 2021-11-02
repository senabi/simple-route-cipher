import { useState } from "react";
import "./App.css";

function App() {
  const [secret, setSecret] = useState(null);
  const [path, setPath] = useState(null);
  const [text, setText] = useState("Enter message");
  const [output, setOutput] = useState("Encrypted message");
  const [position, setPosition] = useState(0);

  const handleKey = (e) => {
    console.log(e.target.value);
    setSecret(e.target.value);
  };

  const handlePath = (e) => {
    console.log(e.target.value);
    setPath(e.target.value);
  };

  const handleText = (e) => {
    console.log(e.target.value);
    setText(e.target.value);
  };

  const handleEncrypt = (e) => {
    console.log("encrypting...");

    e.preventDefault();
    const data = { text, secret, path, position };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch("https://jsonplaceholder.typicode.com/posts", requestOptions)
      .then((response) => response.json())
      .then((res) => console.log(res));
  };

  const handleDecrypt = () => {
    console.log("decrypting...");
  };

  const handleCopy = () => {
    setText(output);
  };

  const handlePosition = (e) => {
    console.log(e.target.value);
    setPosition(e.target.value);
  };

  const handleReset = () => {
    setSecret(null);
    setPath(null);
    setText("Enter message");
    setOutput("Encrypted message");
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>Secret key:</p>
        <select onChange={(e) => handleKey(e)} defaultValue="">
          <option value="">select key</option>
          <option value={3}>3</option>
          <option value={4}>4</option>
          <option value={5}>5</option>
          <option value={6}>6</option>
          <option value={7}>7</option>
          <option value={8}>8</option>
          <option value={9}>9</option>
        </select>
        <br />
        <p>The shape of the path:</p>
        <input
          type="radio"
          name="buttonPathType"
          value="anticlockwise"
          onClick={(e) => handlePath(e)}
        />{" "}
        Anti Clockwise
        <input
          type="radio"
          name="buttonPathType"
          value="clockwise"
          onClick={(e) => handlePath(e)}
        />{" "}
        Clockwise
        <br />
        <br />
        <p>Initial position:</p>
        <select onChange={(e) => handlePosition(e)} defaultValue="">
          <option value="">select position</option>
          <option value={0}>0</option>
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
        </select>
        <br />
        <p>Input Message:</p>
        <textarea
          onChange={(e) => handleText(e)}
          type="text"
          value={text}
        ></textarea>
        <br />
        <button onClick={(_) => handleEncrypt(_)}>Encrypt</button>
        <br />
        <button onClick={(_) => handleDecrypt()}>Decrypt</button>
        <br />
        <p>Output Message:</p>
        <textarea value={output} type="text"></textarea>
        <br />
        <button onClick={(_) => handleReset()}>Reset</button>
        <br />
        <button onClick={(_) => handleCopy()}>Copy Output to Input</button>
        <p>secret: {secret}</p>
        <p>path: {path}</p>
        <p>position: {position}</p>
        <p>input: {text}</p>
        <p>output: {output}</p>
      </header>
    </div>
  );
}

export default App;

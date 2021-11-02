import { useState } from "react";
import "./App.css";

function App() {
  const [block, setBlock] = useState(null);
  const [path, setPath] = useState(null);
  const [text, setText] = useState("Enter message");
  const [output, setOutput] = useState("Encrypted message");
  const [position, setPosition] = useState(0);
  const [text2, setText2] = useState("Enter 2nd message");
  const [output2, setOutput2] = useState("Encrypted message");
  const [num, setNum] = useState(0);

  const handleKey = (e) => {
    console.log(e.target.value);
    setBlock(e.target.value);
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
    const data = { text, block, path, position };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    //fetch("https://jsonplaceholder.typicode.com/posts", requestOptions)
    fetch("http://localhost:5000/api/encrypt", requestOptions)
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setOutput(res["cipherText"]);
      });
  };

  const handleDecrypt = (e) => {
    console.log("decrypting...");
    e.preventDefault();
    const data = { text, block, path, position };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch("http://localhost:5000/api/decrypt", requestOptions)
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setOutput(res["decipherText"]);
      });
  };

  const handleEncrypt2 = (e) => {
    console.log("encrypting...");

    e.preventDefault();
    const data = { text2, num };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    //fetch("https://jsonplaceholder.typicode.com/posts", requestOptions)
    fetch("http://localhost:5000/api/encrypt2", requestOptions)
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setOutput2(res["cipherText"]);
      });
  };

  const handleDecrypt2 = (e) => {
    console.log("decrypting...");
    e.preventDefault();
    const data = { text2, num };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch("http://localhost:5000/api/decrypt2", requestOptions)
      .then((response) => response.json())
      .then((res) => {
        console.log(res);
        setOutput2(res["decipherText"]);
      });
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

  const handleReset2 = () => {
    setText2("Enter message");
    setOutput2("Encrypted message");
    setNum(0);
  };

  const handleCopy2 = () => {
    setText2(output2);
  };

  const handleNum = (e) => {
    console.log(e.target.value);
    setNum(e.target.value);
  };

  const handleText2 = (e) => {
    console.log(e.target.value);
    setText2(e.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>Block size:</p>
        <select onChange={(e) => handleKey(e)} defaultValue="">
          <option value="">select size</option>
          <option value={1}>1</option>
          <option value={2}>2</option>
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
        <button onClick={(_) => handleDecrypt(_)}>Decrypt</button>
        <br />
        <p>Output Message:</p>
        <textarea value={output} type="text"></textarea>
        <br />
        <button onClick={(_) => handleReset()}>Reset</button>
        <br />
        <button onClick={(_) => handleCopy()}>Copy Output to Input</button>
        <p>block: {block}</p>
        <p>path: {path}</p>
        <p>position: {position}</p>
        <p>input: {text}</p>
        <p>output: {output}</p>
        <p>==============================================================</p>
        <p>Transposicion serie</p>
        <p>Input: </p>
        <textarea
          onChange={(e) => handleText2(e)}
          type="text"
          value={text2}
        ></textarea>
        <br />
        <br />
        <p>Num: </p>
        <select onChange={(e) => handleNum(e)} defaultValue="">
          <option value="">select position</option>
          <option value={0}>0</option>
          <option value={1}>1</option>
        </select>
        <br />
        <br />
        <button onClick={(_) => handleEncrypt2(_)}>Encrypt</button>
        <br />
        <button onClick={(_) => handleDecrypt2(_)}>Decrypt</button>
        <br />
        <br />
        <p>Output: </p>
        <textarea type="text" value={output2}></textarea>
        <br />
        <button onClick={(_) => handleReset2()}>Reset</button>
        <br />
        <button onClick={(_) => handleCopy2()}>Copy Output to Input</button>
        <br />
        <p>input: {text2}</p>
        <p>num: {num}</p>
        <p>output: {output2}</p>
      </header>
    </div>
  );
}

export default App;

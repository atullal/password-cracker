import logo from './logo.svg';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import './App.css';
import { useEffect, useState } from 'react';
import { getAvailableClients, submitForm, addClientsApi, wsApi, getStatistics } from './Api';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import ProgressBar from 'react-bootstrap/ProgressBar';

function App() {
  const [md5, setMd5] = useState("");
  const [availableClients, setAvailableClients] = useState([]);
  const [selectedClients, setSelectedClients] = useState([]);
  const [addClientsList, setAddClientsList] = useState([]);
  const [result, setResult] = useState();
  const [startTime, setStartTime] = useState();
  const [endTime, setEndTime] = useState();
  const { sendMessage, lastMessage, readyState } = useWebSocket(wsApi);
  const [messageHistory, setMessageHistory] = useState([]);
  const [err, setErr] = useState();
  const [requestId, setRequestId] = useState();
  const [progress, setProgress] = useState(0);
  const [stats, setStats] = useState();
  
  useEffect(() => {
    getAvailableClients().then((res) => {
      setAvailableClients(res.data["available_clients"]);
    });
  }, [])

  useEffect(() => {
    if (lastMessage !== null) {
      console.log(lastMessage);
      console.log(lastMessage.data);
      try {
        let response = JSON.parse(lastMessage.data.replace(/'/g, '"'));
        console.log(response);
        if(response.requestId) {
          setRequestId(response.requestId);
          getAvailableClients().then((res) => {
            setAvailableClients(res.data["available_clients"]);
          });
        }
        if(response.password) {
          console.log(response.password);
          setEndTime(new Date());
          setResult(response.password);
          setProgress(100);
          getStatistics(requestId, response.password).then((res) => {
            console.log(res.data);
            setStats(res.data);
          })
        }
        if(response.success === 0) {
          if(progress <= 100) {
            setProgress(progress + 1.923);
          }
          console.log(response.file);
        }
        if(response.err) {
          setErr(response.err);
        }
      } catch (error) {
        
      }
      setMessageHistory((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage, setMessageHistory]);

  const md5Input = (e) => {
    setMd5(e.target.value);
  };

  const onSubmit = (e) => {
    e.preventDefault();
    setStartTime(new Date());
    sendMessage(JSON.stringify({
      "task": "password",
      "hash": md5,
      "clients": selectedClients
    }));
  }

  const addClientsSubmit = (e) => {
    if(e && e.preventDefault) {
      e.preventDefault();
    }
    
    if(addClientsList && addClientsList.length) {
      sendMessage(JSON.stringify({
        "task": "add",
        "hash": md5,
        "clients": addClientsList,
        "requestId": requestId
      }));
    }
  }

  const onCheckboxChange = (e, client) => {
    const clientFoundInd = selectedClients.findIndex((selectedClient) => selectedClient === client);
    
    if(clientFoundInd !== -1) {
      setSelectedClients(selectedClients.splice(clientFoundInd, 1))
    } else {
      setSelectedClients([...selectedClients, client])
    }
  }

  const onAddCheckboxChange = (e, client) => {
    const clientFoundInd = addClientsList.findIndex((selectedClient) => selectedClient === client);
    
    if(clientFoundInd !== -1) {
      setAddClientsList(addClientsList.splice(clientFoundInd, 1))
    } else {
      setAddClientsList([...addClientsList, client])
    }
  }

  return (
    <div className="App">
      <div className='container'>
        <div className='top-margin'>
          <div className='row'>
            <div className='col-md-3'></div>
            <div className='col-md-6'>
              <div className='main-card'>
              <h1 className='app-header'>Password Cracker</h1>
              {
                !requestId ? <Form onSubmit={(e) => {onSubmit(e)}}>
                  <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>MD5 Hash</Form.Label>
                    <Form.Control type="text" placeholder="Enter hash"  onChange={(e)=>{md5Input(e)}} />
                  </Form.Group>
                  <div className='available-clients'>
                    <Form.Group className="mb-3" controlId="formClients">
                      <Form.Label>Clients</Form.Label>
                      {availableClients.map((client, ind) => {
                        return (<Form.Check 
                          key={ind}
                          onChange={(e) => {onCheckboxChange(e, client)}}
                          disabled={client.inUse}
                          type='checkbox'
                          id={`default-${ind}`}
                          label={`Client: ${client.address}, Port: ${client.port}`}
                        />);
                      })}
                    </Form.Group>
                  </div>
                  <Button className="mt-3 submit-button" variant="light" type="submit">
                  →
                  </Button>
                </Form> : <div>
                  {!result ?<><h5>We are working hard to crack your MD5 Hash and get your password.</h5>
                  <br/></>: <><h5>Done! we have got your results.</h5>
                  <br/></> }
                  
                  <ProgressBar animated now={progress} />
                  {!result ? <>
                  <Form>
                    <p>You can add more clients to speed up the process.</p>
                    <Form.Group className="mb-3" controlId="formClients">
                      <Form.Label>Clients</Form.Label>
                      {availableClients.map((client, ind) => {
                        return (<Form.Check 
                          key={ind}
                          onChange={(e) => {onAddCheckboxChange(e, client)}}
                          disabled={client.inUse}
                          type='checkbox'
                          id={`default-${ind}`}
                          label={`Client: ${client.address}, Port: ${client.port}`}
                        />);
                      })}
                    </Form.Group>
                    <Button className="mt-3" variant="light" onClick={(e) => {addClientsSubmit(e)}}>
                      Add clients
                    </Button>
                  </Form></> : <>
                  <br/>
                  <h5>Results</h5>
                  <br/>
                  <p>Password: {result}</p>
                  <p>Start Time: {startTime.toTimeString()}</p>
                  <p>End Time: {endTime.toTimeString()}</p>
                  <p>Total time: {((endTime.getTime() - startTime.getTime()) / 1000).toFixed(3)} seconds</p>
                  { stats ? <>
                    <p>Hashes processed: {stats.totalHashes}</p>
                    <p>Number of files processed: {stats.numberOfFiles}</p>
                    <p>Total time to process hashes: {stats.totalTime.toFixed(3)} seconds</p>
                    <p>Time to process each hash: {(stats.totalTime * 1000000/stats.totalHashes).toFixed(3)} μs</p>
                    <p>Time to process each file: {(stats.totalTime* 1000000/stats.numberOfFiles).toFixed(3)} μs</p>
                  </> : <></>}
                  </>}
                  
                </div>
              }
              </div>
            </div>
            <div className='col-md-3'>
            </div>
          </div>
        </div>
      </div>
    
    </div>
  );
}

export default App;

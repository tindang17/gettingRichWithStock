import * as React from 'react';
import { VictoryBar, VictoryStack, VictoryAxis, VictoryLabel} from "victory";
import './App.css';

const dataA = [
  { title: "TSLA", y: 51, x: 1 },
  { title: "Short SPY", y: 40, x: 2 },
  { title: "Long VXX", y: 38, x: 3},
  { title: "Gay Bear", y: 37, x: 4 },
  { title: "Yolo Bet", y: 25, x: 5 },
  { title: "DIS", y: 19, x: 6 },
  { title: "Long AAPL", y: 15, x: 7 },
  { title: "Fed cut rates", y: 13, x: 8 },
  { title: "Phone", y: 12, x: 9 }
];

const width = 1000;
const height = 1000;
const padding = { top: 80, bottom: 80, left: 20, right: 20 };

class App extends React.Component<any, any, any> {
  constructor(props: any) {
    super(props)

    this.state = {
      data: null
    }
  }
  componentDidMount() {
    let count = 0
    const dataB = dataA.map(point => {
      const y = Math.round(point.y + 3 * (Math.random() - 0.5));
      count++
      console.log(count);

      return { count, ...point};
    });

    this.setState({data: dataB})

  }

  render() {
    const graph = (<svg viewBox={`0 500 ${width} ${height}`}
      style={{ width: "100%", height: "auto" }}
    >
      <VictoryStack horizontal
        standalone={false}
        domain={{ x: [0, 30], y: [0, 100] }}
        // padding={padding}
        height={height}
        width={width}
        style={{ data: { width: 20 }, labels: { fontSize: 11 } }}

      >
        <VictoryBar
          style={{ parent: { fill: "tomato" } }}
          data={dataA}
          y={(data) => 0}
          labels={({ datum }) => (`${datum.title}`)}
        />
        <VictoryBar
          style={{ data: { fill: "orange" } }}
          data={this.state.data}
          labels={({ datum }) => (`${Math.abs(datum.count)}%`)}
        />
      </VictoryStack>

      <VictoryAxis dependentAxis
        height={height}
        width={width}
        padding={padding}
        style={{
          axis: { stroke: "transparent" },
          ticks: { stroke: "transparent" },
          tickLabels: { fontSize: 11, fill: "black" }
        }}

        tickLabelComponent={<VictoryLabel x={250} textAnchor="middle" />}
        tickValues={dataA.map(point => point.x).reverse()}
      />
    </svg>)

    if (this.state.data != null) {
      console.log('this')

    return <div style={{backgroundColor: 'blue'}}>
      <div style={{ backgroundColor: 'red', width: '80%' }}
      >
        {graph}
      </div>
    </div>
    } else {
      return null
    }
  }
}

export default App;

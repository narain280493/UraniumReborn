
class PreferenceMatrix extends React.Component {
    constructor(props){
        super(props);
        this.colHeaders = this.props.colHeaders;
        this.rowHeaders = this.props.rowHeaders;
        this.sProjPrefs = this.props.projPrefs;
        this.tCName = this.props.classNames;
    }
    createColHeader(){
        return (<thead>
        <tr>
            <th>&nbsp;</th>
            {this.colHeaders.map( (e) => {return(<th id={e["id"]} style={{textAlign:"center"}}> {e["Title"]} </th>)})}
        </tr>
        </thead>)
    }
    createRowHeader(){
        return (<tbody>
                {this.rowHeaders.map( (re) => {
                    var prefCols = [];
                    var pref = this.sProjPrefs.find( (pe) => pe["stuapp"] == re["id"]);
                    this.colHeaders.map( (ce) => {
                        var iter = ["1","2","3","4","5"];
                        var val = iter.find( (con) => ce["id"]==pref["ProjectPreference"+con]);
                        if(val)
                            prefCols.push(<td>{val}</td>);
                        else
                            prefCols.push(<td>&nbsp;</td>);
                    });
                    return(<tr style={{textAlign:"center"}}>
                        <td id={re["id"]}> {re["LastName"] + " " + re["FirstName"]} </td>
                        {prefCols}
                    </tr>);
                })}
            </tbody>)
    }
    render(){
        return(<table className={this.tCName}>
            {this.createColHeader()}
            {this.createRowHeader()}
        </table>)
    }
}

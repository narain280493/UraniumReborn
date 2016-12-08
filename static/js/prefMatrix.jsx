
class PreferenceMatrix extends React.Component {
    constructor(props){
        super(props);
        this.colHeaders = this.props.colHeaders;
        this.rowHeaders = this.props.rowHeaders;
        this.sProjPrefs = this.props.projPrefs;
        this.assignedProjs = this.props.assignedProjs;
        this.tCName = this.props.classNames;
    }
    createColHeader(){
        return (<thead>
        <tr>
            <th style={{textAlign:"center"}}>Preferences</th>
            <th style={{textAlign:"center"}}>Assigned Project</th>
            {this.colHeaders.map( (e) => {return(<th id={e["id"]} style={{textAlign:"center"}}> {e["Title"]} </th>)})}
        </tr>
        </thead>)
    }
    createRowHeader(){
        return (<tbody>
                {this.rowHeaders.map( (re,i) => {
                    var prefCols = [];
                    var aP = this.colHeaders.find( (x) => {
                        if(i < this.assignedProjs.length)
                            return x["id"]==this.assignedProjs[i];
                        else
                            return false;
                    });
                    var Title = "Not Assigned/Eliminated";
                    if(aP)
                        Title = aP["Title"];
                    var pref = this.sProjPrefs.find( (pe) => pe["stuapp"] == re["id"]);
                    if(pref) {
                        this.colHeaders.map((ce) => {
                            var iter = ["1", "2", "3", "4", "5"];
                            var val = iter.find((con) => ce["id"] == pref["ProjectPreference" + con]);
                            if (val)
                                prefCols.push(<td>{val}</td>);
                            else
                                prefCols.push(<td>&nbsp;</td>);
                        });
                    }else{
                        this.colHeaders.map((ce) => {
                            prefCols.push(<td>&nbsp;</td>);
                        });
                    }
                    return(<tr style={{textAlign:"center"}}>
                        <td id={re["id"]}> {re["LastName"] + " " + re["FirstName"]} </td>
                        <td> {Title} </td>
                        {prefCols}
                    </tr>);
                })}
            </tbody>)
    }
    render(){
        return(<table className={this.tCName}>
            {this.createColHeader()}
            {this.createRowHeader()}
        </table>);
    }
}

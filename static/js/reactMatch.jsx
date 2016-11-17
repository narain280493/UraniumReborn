var Table = Reactabular.Table;
var sort = Reactabular.sort;
var Search = Reactabular.Search;
var search = Reactabular.search;
var orderBy = _.orderBy;

class MatchModal extends React.Component {
    constructor(props){
        super(props);
        this.pOpts = this.props.opts
    }

    clickEvent(){
        alert("Modify is still in construction stage. Please check back again later")
    }

    render(){
        return (
        <div className="modal-dialog modal-lg" role="document">
            <div className="modal-content">
                <div className="modal-header">
                    <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h5 className="modal-title" id="matchModalLabel"><b> Modify Assignment </b></h5>
                </div>
                <div className="modal-body">
                    <label>Student Name:</label>
                    <p> {this.props.rowData["Student Name"]} </p>
                    <label >Assigned Project:</label>
                    <div>
                       <select className="form-control"> {
                          this.pOpts.map((pDet, i) => {
                             if(pDet["Title"]!=this.props.rowData["Project Name"]){
                                return (<option key={pDet["id"]}> {pDet["Title"]}</option>)
                             }else{
                                return (<option key={pDet["id"]} selected="selected"> {pDet["Title"]} </option>)
                             }
                             })
                          }
                       </select>
                    </div>
                </div>
                <div className="modal-footer">
                    <button type="button" className="btn btn-primary" onClick={this.clickEvent} data-dismiss="modal">Modify</button>
                </div>
            </div>
        </div>
    );
    }
}


class MatchesTable extends React.Component {
    constructor(props) {
        super(props);
        const getSortingColumns = () => this.state.sortingColumns || {};
        const sortable = sort.sort({
            getSortingColumns,
            onSort: selectedColumn => {
                this.setState({
                    sortingColumns: sort.byColumns({
                        sortingColumns: this.state.sortingColumns, selectedColumn
                    })
                })
            }
        });
        const resetable = sort.reset({
            event: 'onDoubleClick',
            getSortingColumns,
            onReset: ({sortingColumns}) => this.setState({sortingColumns})
        });
        this.state = {
            // Sort the first column in a descending way by default.
            // "asc" would work too and you can set multiple if you want.
            sortingColumns: {
                0: {
                    direction: 'desc',
                    position: 0
                }
            },
            columns: [
                {
                    property: 'Student Name',
                    header: {
                        label: 'Student Name',
                        transforms: [sortable],
                        format: sort.header({
                            sortable,
                            getSortingColumns
                        })
                    }
                },
                {
                    property: 'Project Name',
                    header: {
                        label: 'Assigned Project',
                        transforms: [sortable],
                        format: sort.header({
                            sortable,
                            getSortingColumns
                        })
                    }
                }
            ],
            rows: this.props.crows
        };
        this.onRow = this.onRow.bind(this)
    }

    render(){
        const {searchColumn, rows, columns, query, sortingColumns} = this.state;
        const searchedRows = search.multipleColumns({ columns, query })(rows);
        const sortedRows = sort.sorter({
            columns,
            sortingColumns,
            sort: orderBy
        })(searchedRows);
        return(
            <div>
            <div className="search-container well">
            <span className="glyphicon glyphicon-search"></span>
            <Search
        column={searchColumn}
        query={query}
        columns={columns}
        rows={rows}
        onColumnChange={searchColumn => this.setState({ searchColumn })}
        onChange={query => this.setState({ query })}
    />
    </div>
        <Table.Provider className="table table-striped well table-hover" columns={columns}>
            <Table.Header />
            <Table.Body rows={sortedRows} rowKey="id" onRow={this.onRow}/>
    </Table.Provider>
        </div>
    );
    }

    onRow(row, { rowIndex }) {
        return {
            className: 'selected-row',
            onClick: () => {
                $("#" + this.props.modalID).empty();
                ReactDOM.render(<MatchModal rowData={row} opts={this.props.opts} />,
                    document.getElementById(this.props.modalID));
                $("#" + this.props.modalID).modal("toggle")
            }
        };
    }
}
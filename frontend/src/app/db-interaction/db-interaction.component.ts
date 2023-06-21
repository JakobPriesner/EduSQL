import {Component} from '@angular/core';
import {SqlService} from "../../lib/services/api/sql.service";
import {SqlResult} from "../../lib/models/sqlResult";
import {SelectAllSqlResult} from "../../lib/models/selectAllSqlResult";

@Component({
  selector: 'app-db-interaction',
  templateUrl: './db-interaction.component.html',
  styleUrls: ['./db-interaction.component.scss']
})
export class DbInteractionComponent {
  code: string = '';
  history: Array<[string, SqlResult]> = [];

  constructor(private sqlService: SqlService){

  }
  onCodeChange(code: string): void{
    this.code = code;
  }

  executeSql():void{
    this.sqlService.executeSql(this.code).subscribe(result => {
        this.history.push([this.code, result]);
    });
  }

  isArray(obj : any) : boolean {
    return Array.isArray(obj);
  }

  getRowValue(row: {[key: string]: any}, columnKey: string): any {
    return row[columnKey];
  }

  getFirstElement(arr: any): any {
    return Array.isArray(arr) ? arr[0] : null;
  }

}

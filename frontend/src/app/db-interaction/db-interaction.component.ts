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

  executeSql():void{
    this.sqlService.executeSql(this.code).subscribe(result => {
        this.history.push([this.code, result]);
        this.code = '';
    });
  }
}

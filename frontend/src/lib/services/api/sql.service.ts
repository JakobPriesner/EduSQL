import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";

import {Observable} from "rxjs";
import {SqlExecutionPayload} from "../../models/sqlExecutionPayload";
import {DbUserStore} from "../../stores/db-user.store";
import {SqlResult} from "../../models/sqlResult";
import {UpdateSqlResult} from "../../models/updateSqlResult";
import {DeleteSqlResult} from "../../models/deleteSqlResult";
import {InsertSqlResult} from "../../models/insertSqlResult";
import {SelectAllSqlResult} from "../../models/selectAllSqlResult";

@Injectable({
    providedIn: 'root'
})
export class SqlService {

    constructor(private httpClient: HttpClient, private dbUserStore: DbUserStore) {
    }
    executeSql(sql: string): Observable<SqlResult>{
        let payload: SqlExecutionPayload = {username: this.dbUserStore.username, password: this.dbUserStore.password, sqlStatement: sql};
        if(sql.toLowerCase().trim().startsWith("update")){
            return this.httpClient.post<UpdateSqlResult>("/api/sqls/update", payload);
        }
        if(sql.toLowerCase().trim().startsWith("delete")){
            return this.httpClient.post<DeleteSqlResult>("/api/sqls/delete", payload);
        }
        if(sql.toLowerCase().trim().startsWith("insert")){
            return this.httpClient.post<InsertSqlResult>("/api/sqls/insert", payload);
        }
        return this.httpClient.post<SelectAllSqlResult>("/api/sqls/load-all", payload);

    }
}

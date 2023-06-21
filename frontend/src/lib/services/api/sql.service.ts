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
import {CookieService} from "../cookie.service";

@Injectable({
    providedIn: 'root'
})
export class SqlService {

    constructor(private httpClient: HttpClient, private dbUserStore: DbUserStore, private cookieService: CookieService) {
    }
    executeSql(sql: string): Observable<SqlResult>{
        let payload: SqlExecutionPayload = {username: this.dbUserStore.username, password: this.dbUserStore.password, sqlStatement: sql};
        if(sql.toLowerCase().trim().startsWith("update")){
            return this.httpClient.post<SqlResult>("/api/sqls/update?uuid="+this.cookieService.getCookie("uuid"), {...payload});
        }
        if(sql.toLowerCase().trim().startsWith("delete")){
            return this.httpClient.post<SqlResult>("/api/sqls/delete?uuid="+this.cookieService.getCookie("uuid"), {...payload});
        }
        if(sql.toLowerCase().trim().startsWith("insert")){
            return this.httpClient.post<SqlResult>("/api/sqls/insert?uuid="+this.cookieService.getCookie("uuid"), {...payload});
        }
        return this.httpClient.post<SqlResult>("/api/sqls/load-all?uuid="+this.cookieService.getCookie("uuid"), {...payload});

    }
}

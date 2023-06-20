import {SqlResult} from "./sqlResult";

export interface InsertSqlResult extends SqlResult{
    operation: string
    result?: number
    errors: string
}
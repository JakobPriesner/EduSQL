import {SqlResult} from "./sqlResult";

export interface DeleteSqlResult extends SqlResult{
    operation: string
    result?: number
    errors: string
}
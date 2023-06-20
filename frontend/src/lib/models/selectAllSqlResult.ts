import {SqlResult} from "./sqlResult";

export interface SelectAllSqlResult extends SqlResult{
    operation: string
    result?: Array<Map<string, any>>
    errors: string
}
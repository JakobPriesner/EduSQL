import {SqlResult} from "./sqlResult";

export interface SelectSingleSqlResult extends SqlResult{
    operation: string
    result?: Map<string, any>
    errors: string
}
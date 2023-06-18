import {Injectable} from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class DbUserStore {
  public username: string = "";
  public password: string = "";
}

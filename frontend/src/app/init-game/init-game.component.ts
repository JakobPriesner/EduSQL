import { Component } from '@angular/core';
import {UsersService} from "../../lib/services/api/users.service";
import {CookieService} from "../../lib/services/cookie.service";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-init-game',
  templateUrl: './init-game.component.html',
  styleUrls: ['./init-game.component.css']
})
export class InitGameComponent {

  public isLoading: boolean = false;

  constructor(private userService: UsersService,
              private cookieService: CookieService,
              private snackBar: MatSnackBar) {
  }

  submit(uuidInput: string) : void {
    this.isLoading = true;
    if (uuidInput) {
      this.verifyUser(uuidInput);
    } else {
      this.registerUser();
    }
  }

  verifyUser(uuidInput: string) : void {
    this.userService.checkIfUserExists(uuidInput).subscribe(result => {
      console.log("Check if user exists")
      if (result.exists) {
        this.cookieService.createCookie("uuid", uuidInput, 7);
      } else {
        this.snackBar.open("Kein Projekt mit der UUID gefunden! Versuche es erneut oder beginne ein neues Spiel.")
      }
      this.isLoading = false;
    });
  }

  registerUser() : void {
    this.userService.registerUser().subscribe(result => {
      console.log("Create cookie: " + result.userUuid);
      this.cookieService.createCookie("uuid", result.userUuid, 7);
      this.isLoading = false;
    })
  }
}

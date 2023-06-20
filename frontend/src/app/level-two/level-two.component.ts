import { Component } from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {AbstractControl} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {LevelValidationResult} from "../../lib/models/levelValidationResult";

@Component({
  selector: 'app-level-two',
  templateUrl: './level-two.component.html',
  styleUrls: ['./level-two.component.css']
})
export class LevelTwoComponent {
  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";
  countProf?: number = undefined;

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore) {

  }

  validateDbUserLoginTask(stepper: MatStepper) {
    // let dbUser: string = (this.userDataStore.firstName.at(0) + "_" + this.userDataStore.lastName).toLowerCase();
    // console.log(dbUser)
    // let validationResult = this.localDbUserValidator.validateLoggedInAsUser(2, 2, dbUser);
    // this.errorMessage = validationResult.message;
    // if (validationResult.isValid) {
    //   this.updateHighestValidationStep(validationResult.level, stepper);
    // }

    this.updateHighestValidationStep("2.2", stepper); // todo: delete
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

  validateCountProfTask(to: string, stepper: MatStepper) {
    if (this.countProf == undefined)
    {
      this.errorMessage += "The input field is empty!";
      return;
    }
    let payload = new Map<string, number>([
      ["answer", this.countProf]
    ]);
    this.validationService.validateTaskWithPayload(3, 1, payload).subscribe(result => {
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to)) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      }
    });
  }
}

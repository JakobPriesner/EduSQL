import {Component, OnInit} from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {MatStepper} from "@angular/material/stepper";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {InboxService} from "../../lib/services/api/inbox.service";

@Component({
  selector: 'app-level-one',
  templateUrl: './level-one.component.html',
  styleUrls: ['./level-one.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelOneComponent implements OnInit{
  errorMessage: string = "";
  highestValidatedLevel: string = this.cookieService.getCookie("highestValidatedLevel") ?? "0.0";

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore,
              public inboxService: InboxService) {
    this.highestValidatedLevel = this.cookieService.getCookie("highestValidatedLevel") ?? "0.0";
  }

  ngOnInit() {
  }

  validateTask(task: number, stepper: MatStepper) : void {
    this.validationService.validateTask(1, task).subscribe(result => {
      this.errorMessage = result.message;
      if (result.isValid) {
        this.highestValidatedLevel = result.level;
        stepper.next();
        this.errorMessage = "";
      }
    });
  }

  validateWithPersonInfoAsPayload(task: number, stepper: MatStepper) : void {
    let payload: { [key: string]: any } = {
      firstName: this.userDataStore.firstName,
      lastName: this.userDataStore.lastName
    };
    this.validationService.validateTaskWithPayload(1, task, payload).subscribe(result => {
      this.errorMessage = result.message;
      if (result.isValid) {
        this.highestValidatedLevel = result.level;
        stepper.next();
        this.errorMessage = "";
      }
    });
  }

  validateDbUserLoginTask(stepper: MatStepper) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(1, 3, 's_krause');
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (to == "1.2") {
      this.inboxService.addMessage({message:
            "Access data for the secretaryare as follows:\n" +
            "Username = s_krause\n" +
            "Password = uZN3G6eMR5yr9pyq", isSelected: true});
    }
    if (this.highestValidatedLevel.localeCompare(to) <= 0) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    console.log("highest validated level: " + this.highestValidatedLevel);
    stepper.next();
  }

  onSuccessfulLogin(stepper: MatStepper) : void {
    this.errorMessage="";
    stepper.next();
  }
}

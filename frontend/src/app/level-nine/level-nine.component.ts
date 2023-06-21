import { Component } from '@angular/core';
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {MatStepper} from "@angular/material/stepper";

@Component({
  selector: 'app-level-nine',
  templateUrl: './level-nine.component.html',
  styleUrls: ['./level-nine.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelNineComponent {

  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";

  countStudents: number = 0;

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore) {

  }

  ngOnInit() {

  }


  countStudentsWithMax(to: string, stepper: MatStepper, answer: number) : void {


    let payload: { [key: string]: any } = {
      answer: answer
    };
    this.validationService.validateTaskWithPayload(9, 2, payload).subscribe(result => {

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


  onSuccessfulLogin(stepper: MatStepper) : void {
    this.errorMessage="";
    stepper.next();
  }

  validateDbUserLoginTask(stepper: MatStepper) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(9, 1, 's_biedermann');
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

  protected readonly undefined = undefined;
}


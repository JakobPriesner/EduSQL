import {Component, OnInit} from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";

@Component({
  selector: 'app-level-one',
  templateUrl: './level-one.component.html',
  styleUrls: ['./level-one.component.css'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelOneComponent implements OnInit{
  errorMessage: string = "";

  constructor(private cookieService: CookieService,
              private validationService: ValidationService) {

  }

  ngOnInit() {

  }

  cookieValidator(control: AbstractControl): { [key: string]: any } | null {
    const formValue = control.value;
    const cookieValue = this.cookieService.getCookie('cookieName');
    if (cookieValue == null) {
      return { 'cookieExists': false };
    }
    return cookieValue.localeCompare(formValue) >= 0 ? null : { 'stepValidated': false };
  }

  validateStep(task: number) : void {
    this.validationService.validateTask(1, task).subscribe();
  }


}

templates_list = [
    {
        "id": "1",
        "name": "User Registration Welcome Email",
        "template_code": "welcome_user_registration",
        "html": """<!DOCTYPE html>
                    <html lang="en">
                      <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
                        <title>Welcome to Our Platform</title>
                      </head>
                      <body style="margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #e9eff1; padding: 0;">
                        <div style="width: 100%; padding: 40px 20px; box-sizing: border-box;">
                          <div style="background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);">
                            
                            <!-- Header Section -->
                            <div style="background-color: #1e2a47; padding: 25px 20px; text-align: center; border-radius: 10px; font-size: 36px; font-weight: 600; color: #ffb52e; text-transform: uppercase; letter-spacing: 1px;">
                              We're Excited to Have You on Board!
                            </div>

                            <!-- Message Section -->
                            <div style="padding: 20px; color: #3e3e3e; line-height: 1.6;">
                              <h3 style="font-size: 20px; font-weight: 600; color: #1e2a47;">Hi {{data.full_name}},</h3>
                              <p style="font-size: 16px; margin: 15px 0;">We are thrilled to have you as part of our platform. Thank you for choosing us!</p>
                              <p style="font-size: 16px; margin: 15px 0;">To get started, simply click on the link below to log in and explore all the amazing features we've designed just for you:</p>
                              <p style="font-size: 16px; margin: 15px 0;">
                                <a href="https://www.dummywebsite.com" style="color: #ffb52e; font-weight: bold; text-decoration: none;">Click here to login</a>
                              </p>
                              <p style="font-size: 16px; margin: 15px 0;">We hope you enjoy your experience with us. If you need any help or have questions, feel free to reach out.</p>
                            </div>

                            <!-- Footer Section -->
                            <div style="padding-top: 25px; font-size: 16px; color: #3e3e3e;">
                              <p style="margin: 10px 0; font-size: 14px;">Warm Regards,</p>
                              <div style="font-size: 22px; font-weight: 600; color: #1e2a47; padding: 10px 0;">Customer Support Team</div>
                              <div style="font-size: 14px; color: #555555;">1234 Platform St, Suite 100, City, Country</div> <!-- Dummy Address -->
                              <div style="padding-top: 5px; font-size: 14px; color: #555555;">
                                Email: <a href="mailto:support@dummywebsite.com" style="color: #ffb52e; text-decoration: none;">support@dummywebsite.com</a>
                                <span style="display: inline-block; padding: 0 5px; vertical-align: top; color: #888;">|</span>
                                Website: <a href="https://www.dummywebsite.com" style="color: #ffb52e; text-decoration: none;">www.dummywebsite.com</a>
                              </div>
                            </div>

                          </div>
                        </div>
                      </body>
                    </html>
                    """,
        "subject": "Welcome! Let's Get Started",
        "description": "Welcome email sent to user on user registration."
    },
    {
    "id": "2",
    "name": "Forgot Password OTP Email",
    "template_code": "forgot_password_otp",
    "html": """<!DOCTYPE html>
                  <html lang="en">
                    <head>
                      <meta charset="UTF-8">
                      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
                      <title>Reset Your Password</title>
                    </head>
                    <body style="margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #e9eff1; padding: 0;">
                      <div style="width: 100%; padding: 40px 20px; box-sizing: border-box;">
                        <div style="background-color: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);">
                          
                          <!-- Header Section -->
                          <div style="background-color: #1e2a47; padding: 25px 20px; text-align: center; border-radius: 10px; font-size: 36px; font-weight: 600; color: #ffb52e; text-transform: uppercase; letter-spacing: 1px;">
                            Password Reset Request
                          </div>

                          <!-- Message Section -->
                          <div style="padding: 20px; color: #3e3e3e; line-height: 1.6;">
                            <h3 style="font-size: 20px; font-weight: 600; color: #1e2a47;">Hi {{data.full_name}},</h3>
                            <p style="font-size: 16px; margin: 15px 0;">We received a request to reset your password. Please use the OTP below to reset your password:</p>
                            <p style="font-size: 24px; font-weight: bold; color: #ffb52e; margin: 15px 0;">
                              {{data.otp_code}}
                            </p>
                            <p style="font-size: 16px; margin: 15px 0;">If you did not request this, you can safely ignore this email. If you need further assistance, feel free to contact us.</p>
                          </div>

                          <!-- Footer Section -->
                          <div style="padding-top: 25px; font-size: 16px; color: #3e3e3e;">
                            <p style="margin: 10px 0; font-size: 14px;">Best Regards,</p>
                            <div style="font-size: 22px; font-weight: 600; color: #1e2a47; padding: 10px 0;">Customer Support Team</div>
                            <div style="font-size: 14px; color: #555555;">1234 Platform St, Suite 100, City, Country</div> <!-- Dummy Address -->
                            <div style="padding-top: 5px; font-size: 14px; color: #555555;">
                              Email: <a href="mailto:support@dummywebsite.com" style="color: #ffb52e; text-decoration: none;">support@dummywebsite.com</a>
                              <span style="display: inline-block; padding: 0 5px; vertical-align: top; color: #888;">|</span>
                              Website: <a href="https://www.dummywebsite.com" style="color: #ffb52e; text-decoration: none;">www.dummywebsite.com</a>
                            </div>
                          </div>

                        </div>
                      </div>
                    </body>
                  </html>
                  """,
    "subject": "Password Reset Request",
    "description": "Email sent to user with OTP to reset their password."
}

  ]
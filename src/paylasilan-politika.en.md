# Privacy Policy

**Hezarfen Mobile Portfolio**
Operated by ONOUR IMPRAM VENTURES LTD. Last updated 2026-10-26. Effective 2026-10-26.

This privacy policy applies to every mobile application published under the Hezarfen Mobile Portfolio brand. The portfolio currently consists of 41 applications. The full list is in the [App coverage](#app-coverage) section below. Each app respects the practices described here.

## Quick summary

Most of the data you generate while using a Hezarfen app never leaves your device. The apps are designed for offline-first use. Records, scores, and settings live in a local SQLite database on your phone. There is no account system. There is no server we run that stores your personal data.

When you use an ad-supported version of an app, Google AdMob receives an advertising identifier so it can serve ads. When you purchase a premium upgrade, RevenueCat receives an anonymous transaction record. When the app crashes, Sentry receives the crash report. None of these third parties receive your email, your name, or your phone number from us.

BlockZen and StroopSprint do not send crash reports to Sentry; their crash and performance data come from Android vitals in Google Play Console.

## Operator and contact

The operator of every app in this portfolio is ONOUR IMPRAM VENTURES LTD, a company registered in the United Kingdom under company number 17429906, which publishes under the Hezarfen Mobile Portfolio brand and is responsible for the personal data described in this policy.

For privacy questions, data access requests, or deletion requests, write to **{{EMAIL}}** with the subject line "Privacy request" and the name of the app you are asking about. We will respond within thirty days. For EU residents, this address is also the route for GDPR data subject rights. For California residents, this address is the route for CCPA requests.

## App coverage

This policy covers all of the following Hezarfen apps.

### Animal and plant care apps (21)

aqualog, beepulse, birdpulse, bonsaipulse, carnivorouslog, catpulse, chickencoop, compostlog, curepulse, dogpulse, exopetpulse, farmpulse, fermentpulse, ferretcare, horsepulse, insectlog, mushroomlog, plantpulse, reptilelog, rodentpulse, turtlepond.

### Casual mini games (20)

blockzen, catstack, colorsort, doomscroll, dotdash, dropmerge, emojislide, gridrecall, habitloop, impostortest, mergemood, onelink, perfectstop, reflexring, shapematch, speedtap, stroopsprint, tapbalance, vibecheck, wordblitz.

If you are reading this policy from an app store listing of an app that does not appear in the lists above, it is not part of this portfolio and this policy does not apply to it.

## Data we collect

### Stored locally on your device only

Every Hezarfen app uses an embedded SQLite database via the `expo-sqlite` library. Everything you create inside the app lives in that database, on your device, until you delete it.

The kinds of data that live in the local SQLite database vary by app, and may include:

* Care logs you create (feeding times, watering schedules, vet visits, notes).
* Activity records (counts, observations, photos you attach).
* Game progress (highest scores, level completion state, streaks, settings).
* User preferences (theme, language, notification toggles).

We never read from this database. We have no remote backup of it. If you uninstall the app, this data is gone unless you used your phone's own backup feature (Google Drive Backup, iCloud) which is outside our control.

### Sent to Google AdMob (only in ad-supported variants)

If you are using an ad-supported version of a Hezarfen app, the Google AdMob SDK is active. AdMob receives:

* Your Android advertising identifier, or your iOS advertising identifier when you have permitted tracking via App Tracking Transparency.
* Approximate geographic region, derived by Google from your IP address.
* Standard device metadata (OS version, app version, screen size).

This data is used to select which ad to show you. We never see this data ourselves. Google's privacy practices apply at that point. For details, see [Google's Advertising Policies](https://policies.google.com/technologies/ads) and [How Google uses information from sites or apps that use our services](https://policies.google.com/technologies/partner-sites).

Which kind of ads an app requests depends on the app:

* **Only non-personalised ads (BlockZen, StroopSprint, AquaLog, CatPulse, DogPulse, DoomScroll).** The Google Play target audience of these apps includes users under 18. Each of these apps requests only non-personalised ads, for every user and in every region. You are not asked for personalisation consent, and you do not need to refuse it, because personalised ads are never requested.
* **Consent decides (CarnivorousLog, which is for adults aged 18 and over, and every other app in the lists above that is not named in the previous item).** In the European Economic Area, the United Kingdom, and Switzerland, you will see a consent screen on first launch that lets you decline personalised ads. You can change your choice at any time inside the app via Settings, AdMob preferences. Your choice is also propagated to AdMob.

### Sent to RevenueCat (only when you purchase a premium upgrade)

If you tap a buy button to upgrade to premium, RevenueCat handles the receipt validation. RevenueCat receives:

* A random anonymous identifier we never link to you (`$RCAnonymousID`, generated per install).
* Your Google Play or App Store transaction receipt (this is required to verify the purchase).
* Your country, derived from the store you purchased through.

RevenueCat does **not** receive your name, your email, or any other identifier. If you later contact us with a refund request, we will ask you for the transaction id from your Google Play or App Store account so we can match it. We do not have any other lookup path to you.

RevenueCat's privacy practices are described at [revenuecat.com/privacy](https://www.revenuecat.com/privacy).

### Sent to Sentry (only on crash)

BlockZen and StroopSprint do not send crash reports to Sentry; their crash and performance data come from Android vitals in Google Play Console.

If the app crashes or hits an internal error, the `@sentry/react-native` library reports the error to Sentry, in the Frankfurt (EU) data region. Sentry receives:

* A stack trace describing where the crash happened in the code.
* Anonymous breadcrumbs leading up to the crash (which screens you opened, which buttons you tapped, in the last sixty seconds).
* Standard device metadata (OS version, app version, device model).
* A randomly generated install id that resets every time you reinstall the app.

We intentionally do **not** send your name, email, location, or anything you typed into the app. The breadcrumbs are scrubbed by a `beforeSend` filter that removes any free-text payloads.

Crash reports and diagnostics (crash analytics) help us identify and fix bugs. They are retained for ninety days then deleted. Sentry's privacy practices are described at [sentry.io/privacy](https://sentry.io/privacy/).

### Sent to Expo (Hezarfen build infrastructure only)

We build the apps on Expo's EAS Build service. Expo receives the source code we send to it during a build, plus a build artifact. Expo does **not** receive any of your data when you use the app. The Expo relationship is only between us (the developer) and Expo (the build service), not between you and Expo.

### Locale and timezone (from `expo-localization`)

The apps read your phone's selected language and your timezone in order to format dates and pick the right translation. This is read locally from your operating system. It is **not** sent anywhere. The closest data category here is "locale", not "location".

## Data we explicitly do NOT collect

Unless an app explicitly tells you at the moment of asking, no Hezarfen app collects any of the following. If an app uses the data category, the in-app prompt will tell you exactly why and you can decline.

* Precise geographic location (no GPS, no fine location permission requested).
* Your contacts list.
* Your call history.
* Your SMS history.
* Health or fitness data from Apple Health or Google Fit.
* Biometric data.
* Microphone audio.
* Camera images, except photos you yourself attach to an app entry, which then stay in local SQLite.

## Third parties

The complete list of third parties that may receive data, as described above, is:

* **Google AdMob**, for advertising in ad-supported variants. [Google's privacy policy](https://policies.google.com/privacy).
* **RevenueCat**, for in-app purchase receipt validation. [RevenueCat's privacy policy](https://www.revenuecat.com/privacy).
* **Sentry**, for crash reporting in the EU region. [Sentry's privacy policy](https://sentry.io/privacy/).
* **Expo**, for build and update infrastructure (not user-facing). [Expo's privacy policy](https://expo.dev/privacy).

We do not sell your data to anyone. We do not share your data with advertising data brokers. We do not use cross-app or cross-device tracking beyond what AdMob does for ad personalization in the apps that request personalised ads (see "Sent to Google AdMob" above), which you can decline in those apps.

## Your rights

### European Union, United Kingdom, Switzerland (GDPR)

You have the right to access, correct, port, and delete the personal data we hold about you. In practice, because almost everything stays on your device, the "data we hold about you" is essentially nil. The exceptions are:

1. The advertising identifier and ad delivery records held by Google AdMob. To exercise your rights against those records, contact Google directly using the channels in [Google's Advertising Privacy](https://policies.google.com/technologies/ads).
2. The transaction receipt held by RevenueCat. To exercise your rights against those records, contact us with the transaction id and we will forward the deletion request.
3. The crash reports held by Sentry. Crash reports auto-delete after ninety days. To request earlier deletion, contact us with the timestamp of the crash and your phone model and we will purge the matching events.

You also have the right to lodge a complaint with your local data protection authority.

### California (CCPA / CPRA)

You have the right to know what personal information we have, to delete it, to correct it, and to opt out of any sale or sharing. We do not sell or share your data within the meaning of the CCPA. The exceptions above (Google, RevenueCat, Sentry) still apply.

### Right to withdraw consent

In the apps that ask for personalisation consent (the "Consent decides" group under "Sent to Google AdMob"), you can withdraw your consent for personalised ads at any time from the app's Settings screen, AdMob preferences. BlockZen, StroopSprint, AquaLog, CatPulse, DogPulse and DoomScroll do not ask for this consent and request only non-personalised ads, so there is nothing to withdraw in them. You can stop sending crash reports by enabling "Diagnostics opt-out" in Settings, where available.

## Children's privacy

The apps in this portfolio are rated **for users 13 years and older**. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and you believe a child under 13 has used a Hezarfen app and that data was collected, contact us at {{EMAIL}} and we will purge any matching records on a best-effort basis. Because everything stays on the device, the most reliable removal is to uninstall the app.

The apps comply with Google Play's Designed for Families program guidelines and Apple's Kids Category guidelines where applicable, but they are not enrolled in those programs unless the listing on the store explicitly says so.

## International data transfers

The data routed to AdMob, RevenueCat, and Expo may be processed in the United States or in their other regional data centres. The Sentry crash reports are processed in the EU (Frankfurt). Where transfers happen, we rely on Standard Contractual Clauses (SCCs) and the providers' own data transfer mechanisms.

## Security

Local SQLite databases are protected by the operating system's app sandbox. They are not encrypted at the application layer by default, so a determined attacker with physical access to an unlocked device could read them. Use your phone's screen lock to mitigate this.

For data in transit, every connection to AdMob, RevenueCat, Sentry, and Expo uses HTTPS with TLS 1.2 or higher.

## Changes to this policy

When we change this policy, we update the "Last updated" date at the top. Material changes (any change that broadens what data we collect or who receives it) trigger an in-app notification on first launch after the change. Historical versions of this policy are accessible from this URL by inspecting the GitHub repository commit history. The repository is publicly readable.

## Contact

Email: **{{EMAIL}}**

Subject line for privacy requests: "Privacy request - [app name]".

Postal address (only used when legally required): provided on request via email.

---

This document is published as static content. The canonical, machine-readable copy is at https://onourimpram.github.io/portfolio-41/privacy-policy. Any other copy is a derivative and may be out of date.

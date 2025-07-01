/**
 * @typedef {('Global'|'North America'|'Europe'|'Asia'|'South America'|'Africa'|'Oceania')} Region
 */

/**
 * @typedef {('Politics'|'Technology'|'Business'|'Sports'|'Health'|'Entertainment'|'Science')} Topic
 */

/**
 * @typedef {Object} TopicNode
 * @property {string} id             // e.g. 'politics'
 * @property {string} name           // e.g. 'Politics'
 * @property {TopicNode[]} [children] // optional list of subtopics
 */

/**
 * @typedef {Object} Article
 * @property {string} id               // unique identifier
 * @property {string} title
 * @property {string} summary
 * @property {string} source           // e.g. 'BBC', 'CNN'
 * @property {string} url
 * @property {Region} region
 * @property {Topic[]} topics
 * @property {number} biasScore        // computed bias metric
 */

import {pathToRoot} from "../util/path"
import {QuartzComponent, QuartzComponentConstructor, QuartzComponentProps} from "./types"
import {classNames} from "../util/lang"
import {i18n} from "../i18n"

const PageTitle: QuartzComponent = ({fileData, cfg, displayClass}: QuartzComponentProps) => {
    const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
    const baseDir = pathToRoot(fileData.slug!)
    return (
        <h2 className={classNames(displayClass, "page-title")}>
            <img src="static/logo_taigram.svg" width="128" alt=""/>
            <div>
                <a href={baseDir}>{title}</a>
            </div>
        </h2>
    )
}

PageTitle.css = `
.page-title {
  font-size: 1.75rem;
  margin: 0;
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor

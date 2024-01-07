// User
export interface ILoginRegisterFormData {
  username: string
  email: string
  password: string
  confirmPassword: string
}
export interface IUpdatePasswordFormData {
  oldPassword: string
  newPassword: string
  confirmNewPassword: string
}

export interface ILoginRegisterPayload {
  username?: string
  email: string
  password: string
  password_conf?: string
}

export interface IUser {
  categories: ICategory[]
  created_at: string
  email: string
  id: number
  tags: ITag[]
  username: string
}

// Article
export interface IArticle {
  category: ICategory
  comments: string | null
  date_added: string
  favorite: boolean
  html_content: string
  id: number
  read: boolean
  tags: ITag[]
  title: string
  url: string
}

export interface IAddArticleFormData {
  url: string
}

export interface IUpdateArticleFormData {
  category_id?: number
  comments?: string | null
  tags?: string[]
  update_favorite?: boolean
  update_read_status?: boolean
}

export interface IArticlesParams {
  [key: string]: boolean | number | string | undefined
  cat_id?: number
  displaySpinner?: boolean
  favorites?: boolean
  not_read?: boolean
  page: number
  q?: string
  tag_id?: number
}

// Items
export interface ICategory {
  description: string
  id: number
  is_default: boolean
  name: string
  nb_articles: number
  user_id: number
}

export interface ITag {
  id: number
  name: string
  nb_articles: number
  user_id: number
}

export type TItemType = 'categories' | 'tags'

export type TTagColumns = 'id' | 'name' | 'nb_articles'

export type TCategoryColumns = 'id' | 'name' | 'description' | 'nb_articles'

export type TItemQueryColumns = 'name' | 'description'

export interface ISortOrder {
  id: number
  type: number
  name: number
  description: number
  nb_articles: number
}

export interface IItemFormData {
  id: number | null
  type: string
  name: string
  description: string
}

// API
export interface IApiErrorMessage {
  error?: string
  message?: string
}

export interface IPagination {
  has_next: boolean
  has_prev: boolean
  page: number
  pages: number
  total: number
}
